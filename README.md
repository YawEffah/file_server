
# File Server

https://yaweffah.pythonanywhere.com/

File Server is a Django-based web application designed to facilitate the distribution of various documents, such as wedding cards and admission forms. It allows users to sign up, log in, view and download files, search for files, and share files via email. Admins can upload files, and view analytics on downloads and mails sent.

## Table of Contents
- [Features](#features)
- [Usage](#usage)

## Features
### User Features
- **Signup & Login**: Users can sign up and log in using an email and password, with email account verification.
- **Password Reset**: Users can reset their password if they forget it.
- **Feed Page**: Users can see a feed of available files for download.
- **Search**: Users can search for specific files.
- **File Sharing**: Users can send files via email through the platform.

### Admin Features
- **File Upload**: Admins can upload files with titles and descriptions.
- **Analytics**: Admins can view the number of downloads and emails sent for each file.

## Usage
- **Signup**: Navigate to /signup to create a new account.
- **Login**: Navigate to /login to access your account.
- **Feed Page**: View the available files on the feed page after logging in.
- **Search**: Use the search bar on the feed page to find specific files.
- **Share File**: Click on the "Share" button next to a file to email it to someone.
- **Admin Dashboard**: Admins can navigate to /admin_dashboard to upload files and view analytics.
