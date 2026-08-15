# GitHub deployment

1. Upload this repository structure to the `main` branch.
2. In GitHub: Settings → Pages → Build and deployment → Source = GitHub Actions.
3. The `Deploy RIO to GitHub Pages` workflow validates RIO commercial gates first.
4. Only after validation passes does it deploy the `site/` directory.
5. Production verification still requires checking the live URL after deployment.
