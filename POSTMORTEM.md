# 🚨 Postmortem: Deployment Failure During Live Presentation

## ❌ What Happened

During the live presentation of the task processing API, the deployment failed unexpectedly. The API was unresponsive, and the `/tasks` endpoint returned 5xx errors upon invocation.

## 🧠 Root Cause

The failure was caused by a misconfiguration in the CI/CD deployment pipeline. Specifically, a recently added environment variable required for the production Docker image was missing, causing the container to crash during startup.

## 🛠️ Immediate Response

- Checked the logs and identified the environment variable issue.
- Manually added the missing variable to the Fly.io deployment.
- Triggered a rebuild and deployment from GitHub Actions.

## ✔️ Resolution

The redeployment succeeded after the missing configuration was restored. The API became available within 5 minutes of identifying the issue.

## 💡 Lessons Learned

- Critical environment variables should be validated during build time or before deployment.
- Adding automated health checks and rollback mechanisms would prevent downtime.
- Always have a tested fallback image/tag available for emergencies.

## 📈 Preventative Actions

- [ ] Add environment variable checks in the CI pipeline.
- [ ] Implement `/health` endpoint.
- [ ] Store stable image tags for emergency rollbacks.

## 🙌 What Went Well

- Quick identification of the root issue through logs.
- Deployment logs were accessible and informative.
- Manual override via cloud dashboard worked as a last resort.

## 😬 What Could Be Improved

- Lack of pre-deploy validation allowed misconfig to reach production.
- No automated alerts triggered the issue; it was discovered manually.
