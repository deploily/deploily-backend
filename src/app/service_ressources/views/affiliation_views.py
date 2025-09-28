# -*- coding: utf-8 -*-
from flask import flash, redirect, render_template, url_for
from flask_appbuilder import ModelView, action
from flask_appbuilder.actions import action
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder
from app.service_ressources.models.affiliation_model import Affiliation
from app.services.mail_service import send_and_log_email


class AffiliationView(ModelView):
    datamodel = SQLAInterface(Affiliation)
    route_base = "/admin/affiliation"

    list_columns = [
        "created_by",
        "total_price",
        "affiliation_state",
        "phone_number",
        "provider",
        "service_plan",
        "internal_note",
    ]
    base_order = ("id", "desc")
    _exclude_columns = ["created_on", "changed_on"]
    add_exclude_columns = _exclude_columns
    edit_exclude_columns = _exclude_columns

    @action(
        "validate_affiliation",
        "Valider",
        "Confirmer cette affiliation ?",
        "fa fa-check",
        single=True,
    )
    def validate_affiliation(self, affiliations):

        if not isinstance(affiliations, list):
            affiliations = [affiliations]
        validated_count = 0
        for affiliation in affiliations:
            if affiliation.affiliation_state != "pending":
                flash(
                    f"L'affiliation #{affiliation.id} est déjà validée ou non valide.",
                    "warning",
                )
                continue

            # Envoi de l'email au partenaire
            provider = affiliation.provider
            service_plan = affiliation.service_plan
            user = affiliation.created_by

            if provider and provider.mail_partnership:
                provider_email_body = render_template(
                    "emails/provider_affiliation.html",
                    user=user,
                    provider=provider,
                    total_price=affiliation.total_price,
                    service_name=service_plan.service.name,
                    plan_name=service_plan.plan.name,
                )
                send_and_log_email(
                    to=provider.mail_partnership,
                    subject="Nouvelle affiliation via deploily.cloud",
                    body=provider_email_body,
                )

            affiliation.affiliation_state = "confirmed"
            self.datamodel.edit(affiliation)
            validated_count += 1

        flash(
            f"{validated_count} affiliation(s) validée(s) et email(s) envoyé(s).",
            "success",
        )
        return redirect(url_for("AffiliationView.list"))


appbuilder.add_view(
    AffiliationView,
    "Affiliation",
    icon="fa-solid fa-sliders",
    category="Operations",
)
