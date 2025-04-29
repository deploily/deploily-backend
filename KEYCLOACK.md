# Procedure: Enable Terms and Conditions in Keycloak

This guide explains how to require user consent to **Terms of Service** and **Privacy Policy** during registration in Keycloak.

## Steps

1. **Log in to the Keycloak Admin Console.**
2. In the left menu, click **Authentication**.
3. Go to the **Flows** tab.
4. Select the **Registration** flow.
5. Locate the **Terms and Conditions** row in the flow list.
6. Set the dropdown to **Required** for the **Terms and Conditions** step.

    This will enforce the user agreement at registration.

# Procedure: Add Custom Terms Text with Links in Keycloak Localization

This guide explains how to customize the **"Terms and Conditions"** text shown during user registration by adding a localized HTML phrase using **Realm Overrides** in Keycloak.

## Steps

1. Log in to the **Keycloak Admin Console**.

2. In the left menu, go to **Realm settings**.

3. Click on the **Localization** tab.

4. Enable **Internationalization** if it is not already enabled.

5. Click on the **Realm overrides**.

6. Click **Add translation**.

7. Fill out the form as follows:
   - **Key**: `termsText`
   - **Value**:

     ```html
     I agree to the <a href="https://example.com/terms">Terms of Service</a> and <a href="https://example.com/privacy">Privacy Policy</a>.
     ```

     > Replace `https://example.com/terms` and `https://example.com/privacy` with your actual URLs.

8. Click **Save**.

## Result

Users will see the following sentence during registration:

> I agree to the [Terms of Service](https://example.com/terms) and [Privacy Policy](https://example.com/privacy).

Where **Terms of Service** and **Privacy Policy** are clickable links.





