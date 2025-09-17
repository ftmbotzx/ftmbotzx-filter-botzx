# Overview

This is a Telegram media filter bot built with Python and the Pyrogram library. The bot's primary purpose is to automatically index files sent to Telegram channels and provide search functionality through inline queries. It features a comprehensive media management system with premium subscriptions, verification mechanisms, file streaming capabilities, and advanced filtering options.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Core Framework
- **Backend**: Python with Pyrogram for Telegram bot API interactions
- **Database**: MongoDB with Motor async driver for data persistence
- **Storage**: Dual database support for media indexing with fallback mechanisms
- **Async Architecture**: Built on asyncio for concurrent operations

## Database Design
- **Primary Database**: MongoDB instance for main operations (media files, users, groups)
- **Secondary Database**: Backup MongoDB instance for redundancy
- **Collections**: Separate collections for media files, user data, filters, connections, verification records, and referral system
- **Indexing**: Text-based indexing on file names for search functionality

## Authentication & Authorization
- **Admin System**: Role-based access control with configurable admin users
- **Force Subscription**: Channel subscription verification before bot access
- **Premium System**: Time-based premium memberships with expiration tracking
- **Verification System**: User verification with time-limited tokens

## Media Management
- **File Indexing**: Automatic indexing of documents, videos, and audio files from configured channels
- **Search Engine**: Fuzzy search with spell checking using FuzzyWuzzy and AI-powered corrections
- **File Streaming**: Custom streaming server with range request support for media playback
- **Multi-Client**: Support for multiple bot tokens to distribute load

## Content Delivery
- **Streaming Service**: Built-in HTTP server for file streaming with proper MIME type handling
- **Template Engine**: Jinja2-based HTML templates for web interface
- **Shortener Integration**: Support for custom URL shorteners with API integration
- **IMDB Integration**: Movie information fetching with poster support

## Filter System
- **Auto Filter**: Intelligent content filtering based on user queries
- **Global Filters**: Server-wide filter management for admins
- **Custom Filters**: Group-specific filter creation and management
- **Button Support**: Inline keyboard support for interactive responses

## Premium Features
- **Subscription Management**: Time-based premium access with automatic expiration
- **Referral System**: User referral tracking with reward mechanisms
- **Redeem Codes**: Generated codes for premium access distribution
- **Usage Analytics**: Premium user activity tracking and statistics

## Web Interface
- **File Viewer**: Web-based file streaming and download interface
- **Responsive Design**: Mobile-friendly interface with modern CSS frameworks
- **Video Player**: Integrated video player for streaming content
- **Download Portal**: Direct download links with file information

## Configuration System
- **Environment Variables**: Extensive configuration through environment variables
- **Dynamic Settings**: Runtime configuration changes through database
- **Feature Toggles**: Enable/disable features without code changes
- **Multi-Language**: Support for different caption languages and templates

# External Dependencies

## Core Services
- **MongoDB Atlas/Self-hosted**: Primary and secondary database instances
- **Telegram Bot API**: Bot token and API credentials from @BotFather
- **Telegram API**: API ID and hash from my.telegram.org

## Third-Party Integrations
- **IMDB API**: Movie information through Cinemagoer library
- **URL Shorteners**: Configurable shortener services (Shortzy, custom APIs)
- **Cloud Storage**: Optional integration with telegraph for image hosting
- **Analytics**: User tracking and verification statistics

## Python Libraries
- **Pyrogram/Pyrofork**: Telegram client library
- **Motor**: Async MongoDB driver
- **UMongo**: Object Document Mapper for MongoDB
- **Jinja2**: Template engine for web interface
- **aiohttp**: HTTP server and client for streaming
- **FuzzyWuzzy**: Fuzzy string matching for search
- **BeautifulSoup**: HTML parsing for web scraping
- **Pillow**: Image processing for poster handling

## Optional Services
- **Instagram API**: Video download functionality
- **Wikipedia API**: Additional content information
- **Font Services**: Text styling and formatting features
- **Broadcasting**: Mass messaging capabilities for user notifications