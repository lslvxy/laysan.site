<img align="right" width="150" alt="logo" src="https://user-images.githubusercontent.com/5889006/190859553-5b229b4f-c476-4cbd-928f-890f5265ca4c.png">

# Hugo Theme Stack Starter Template

This is a quick start template for [Hugo theme Stack](https://github.com/CaiJimmy/hugo-theme-stack). It uses [Hugo modules](https://gohugo.io/hugo-modules/) feature to load the theme.

It comes with a basic theme structure and configuration. GitHub action has been set up to deploy the theme to a public GitHub page automatically. Also, there's a cron job to update the theme automatically everyday.

## Get started

1. Click *Use this template*, and create your repository on GitHub.
![Step 1](https://user-images.githubusercontent.com/5889006/156916624-20b2a784-f3a9-4718-aa5f-ce2a436b241f.png)

2. Once the repository is created, create a GitHub codespace associated with it.
![Create codespace](https://user-images.githubusercontent.com/5889006/156916672-43b7b6e9-4ffb-4704-b4ba-d5ca40ffcae7.png)

3. Install the build tools below, then run `hugo server` to preview the site.

4. Check `config` folder for the configuration files. You can edit them to suit your needs. Make sure to update the `baseurl` property in `config/_default/config.toml` to your site's URL.

5. GitHub Actions builds pushes and pull requests on `main`.

---

Install Git, Go, Hugo and [standalone Dart Sass](https://gohugo.io/functions/css/sass/#dart-sass). CI uses Go `1.27.x`, Hugo `0.170.1` and Dart Sass `1.108.2`. Make sure the standalone `sass` executable is on `PATH`.

## Update theme manually

Run:

```bash
hugo mod get -u github.com/CaiJimmy/hugo-theme-stack/v4
hugo mod tidy
```

For a future major upgrade, update the import path in `config/_default/module.toml` and follow the theme's migration guide.

## Deploy to another static page hostings

Use the same build tools on the hosting platform, run the production build, and publish the `public` directory.

```bash
hugo --gc --minify
```
