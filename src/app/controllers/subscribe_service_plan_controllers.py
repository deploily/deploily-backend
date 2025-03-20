import logging
from flask import Response, request, jsonify
from flask_appbuilder.api import BaseApi, expose, protect
from flask_jwt_extended import jwt_required
from app import appbuilder, db
from datetime import datetime
from app.services.payment_service import PaymentService
from app.models import Subscribe, ServicePlan, Profile, Payment
from app.utils.utils import get_user

_logger = logging.getLogger(__name__)


class SubscriptionApi(BaseApi):
    resource_name = "service-subscription"

    @protect()
    @jwt_required()
    @expose("/<int:plan_id>/subscribe", methods=["POST"])
    def subscribe_to_plan(self, plan_id):
        """
        Subscribes a user to a service plan.
        ---
        post:
          parameters:
            - in: path
              name: plan_id
              required: true
              schema:
                type: integer
              description: ID of the Service Plan to subscribe to
          responses:
            200:
              description: Subscription successful
              content:
                application/json:
                  schema:
                    type: object
                    properties:
                      message:
                        type: string
                      balance:
                        type: number
                      subscription_id:
                        type: integer
                      payment_id:
                        type: integer
            400:
              description: Invalid request
            402:
              description: Insufficient balance
            500:
              description: Internal Server Error
        """
        try:
            user = get_user()
            if not user:
                return jsonify({"error": "User not found"}), 400

            profile = db.session.query(Profile).filter_by(
                user_id=user.id).first()
            if not profile:
                return jsonify({"error": "Profile not found"}), 400

            plan = db.session.query(ServicePlan).filter_by(id=plan_id).first()
            if not plan:
                return jsonify({"error": "Service Plan not found"}), 400

            if plan.price > profile.balance:
                return jsonify({"error": "Insufficient balance", "balance": profile.balance}), 402
           # TODO REMOVE JUST FOR TESTING
            profile.balance -= plan.price

            subscription = Subscribe(
                name=plan.plan.name,
                start_date=datetime.now(),
                total_amount=plan.price,
                price=plan.price,
                status="paid",
                service_plan_id=plan.id,
                promo_code_id=None
            )
            db.session.add(subscription)
            db.session.flush()

            payment = Payment(
                amount=plan.price,
                payment_method="card",
                subscription_id=subscription.id,
                status="pending"
            )
            db.session.add(payment)
            db.session.commit()

            payment_check = db.session.query(
                Payment).filter_by(id=payment.id).first()
            if not payment_check:
                return jsonify({"error": "Payment ID not found in database"}), 400

            payment_service = PaymentService()
            payment_response = payment_service.post_payement(payment.id)[0]
            print(type(payment_response))
            _logger.error(f"Payment service response: {payment_response}")

            if not isinstance(payment_response, dict):
                return jsonify({"error": "Invalid payment service response"}), 500

            if "ERRORCODE" in payment_response and payment_response["ERRORCODE"] != 0:
                return jsonify({
                    "error": "Payment failed",
                    "message": payment_response.get("ERRORMESSAGE", "Unknown error"),
                    "error_code": payment_response.get("ERRORCODE")
                }), 400

            payment.status = "completed"
            db.session.commit()

            return jsonify({
                "message": "Subscription successful",
                "subscription_id": subscription.id,
                "payment_id": payment.id,
                "amount": payment.amount,
                "user_name": user.username,
                "order_id": payment_response.get("ORDER_ID"),
                "form_url": payment_response.get("FORM_URL")
            }), 200

        except Exception as e:
            _logger.error(f"Error in subscription: {e}", exc_info=True)
            db.session.rollback()
            return jsonify({"error": "Internal Server Error"}), 500


appbuilder.add_api(SubscriptionApi)
