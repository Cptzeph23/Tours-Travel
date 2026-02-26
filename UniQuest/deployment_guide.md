# Render Deployment Guide for UniQuest

This guide provides step-by-step instructions for deploying the UniQuest Django project to Render.

---

### **Step 1: Sign Up for Render & Connect Your Repository**

1.  **Create a Render Account**: If you don't have one, sign up at [render.com](https://render.com).
2.  **Connect Your Git Repository**:
    *   On the Render Dashboard, click **New +** and select **Web Service**.
    *   Connect your GitHub or GitLab account and authorize Render to access your repositories.
    *   Select the repository where your `UniQuest` project is located.

---

### **Step 2: Configure the Web Service**

Render will automatically detect your `render.yaml` file and pre-fill most of the settings. Here’s how to review and confirm them:

1.  **Service Name**: Render will use the name from your `render.yaml` (`UniQuest`).
2.  **Region**: Choose a geographic region close to your users (e.g., Ohio, Frankfurt).
3.  **Branch**: Ensure the correct branch (e.g., `main` or `master`) is selected for deployment.
4.  **Runtime**: This will be automatically set to **Python** based on your `render.yaml`.
5.  **Build & Start Commands**: Render will read these directly from your `render.yaml`:
    *   **Build Command**: `sh build.sh`
    *   **Start Command**: `gunicorn telusko.wsgi:application`
6.  **Instance Type**: Select the **Free** plan to get started.

---

### **Step 3: Create the PostgreSQL Database**

Your `render.yaml` file is configured to automatically create a PostgreSQL database for you.

1.  **Database Creation**: When you create the web service, Render will see the `databases` section in your `render.yaml` and automatically provision a **Free** tier PostgreSQL database named `uniquest-db`.
2.  **Database URL**: Render will also automatically create the `DATABASE_URL` environment variable and link it to your web service, so you don't need to manually copy and paste it.

---

### **Step 4: Set the Secret Key**

You only need to add one environment variable manually:

1.  **Navigate to Environment**: In your web service settings, go to the **Environment** tab.
2.  **Add Secret Key**:
    *   Click **Add Environment Variable**.
    *   **Key**: `SECRET_KEY`
    *   **Value**: Generate a new, secure Django secret key and paste it here. You can use an online generator or run `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'` locally.

---

### **Step 5: Deploy!**

1.  **Create Web Service**: Scroll to the bottom of the page and click **Create Web Service**.
2.  **Monitor Deployment**: Render will now start the deployment process. You can watch the logs in real-time from the **Logs** tab. The first build will take a few minutes as it installs dependencies and runs the build script.
3.  **Go Live**: Once the deployment is successful, you'll see a **Live** status at the top of the page. Your application URL (e.g., `https://uniquest.onrender.com`) will be displayed.