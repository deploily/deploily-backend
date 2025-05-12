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


# ✅ Procedure: Enable Sign in with GitHub in Keycloak

This guide explains how to configure **GitHub login** as an identity provider in Keycloak.

---

## 1. 🧱 Create a GitHub OAuth App

1. Go to [https://github.com/organizations/deploily/settings/applications](https://github.com/organizations/deploily/settings/applications)
2. Click **"New OAuth App"**
3. Fill in the fields:

   - **Application name**: `Deploily Login`
   - **Homepage URL**:  
     ```
     https://auth.dev.deploily.cloud
     ```
   - **Authorization callback URL**:  
     ```
     https://auth.dev.deploily.cloud/realms/myrealm/broker/github/endpoint
     ```

4. Click **Register application**
5. Copy the **Client ID** and **Client Secret**

---

## 2. 🔐 Configure GitHub as Identity Provider in Keycloak

1. Log into the **Keycloak Admin Console**
2. Select your realm (e.g., `myrealm`)
3. Go to **Identity Providers**
4. Click **"Add provider" → GitHub**
5. Fill in the required fields:
   - **Client ID**: (from GitHub)
   - **Client Secret**: (from GitHub)
   - **Default Scopes**: `user:email`
6. Click **Save**

---





