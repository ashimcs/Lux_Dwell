# 🏡 LuxDwell – Automated Premium Real Estate Marketplace and Agent Control Ecosystem

<div align="center">

![Django](https://img.shields.io/badge/Django-6.0.1-green?style=for-the-badge\&logo=django)
![Python](https://img.shields.io/badge/Python-3.13-blue?style=for-the-badge\&logo=python)
![SQLite](https://img.shields.io/badge/SQLite-Database-blue?style=for-the-badge\&logo=sqlite)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5-purple?style=for-the-badge\&logo=bootstrap)

### Premium Real Estate Marketplace with Automated Agent Management

</div>

---

# 📖 Project Abstract

LuxDwell is an enterprise-grade, high-performance real estate marketplace engineered using the Python Django framework. The platform streamlines property transactions among three key stakeholders: System Administrators, Professional Real Estate Agents, and Property Buyers.

The application focuses on reducing listing approval delays, automating property workflows, implementing role-based authorization, and maintaining real-time synchronization of property statuses across the entire marketplace.

The system combines advanced administrative controls, agent-centric management tools, automated listing workflows, inquiry management, and intelligent status propagation into a unified ecosystem designed for scalability and operational efficiency.

---

# 🎯 Objectives

* Digitize and automate real estate operations.
* Eliminate delays in property approval workflows.
* Provide a dedicated workspace for certified agents.
* Enable seamless buyer-agent communication.
* Synchronize property status globally.
* Simplify administrative management.
* Improve transaction transparency.
* Deliver a premium real estate browsing experience.

---

# 👥 User Roles

## 👤 Client / Property Buyer

* Browse available properties.
* Search and filter listings.
* View property details.
* Send inquiries directly to agents.
* Track property availability.

---

## 🏢 Real Estate Agent

* Manage personal property portfolio.
* Create and publish listings.
* Respond to buyer inquiries.
* Track property performance.
* Update property status.
* Manage transactions.

---

## ⚙️ System Administrator

* Manage all users.
* Verify and approve agents.
* Review property listings.
* Delete fraudulent content.
* Manage transactions.
* Monitor platform activities.

---

# ✨ Core Features

## 🔐 Role-Based Access Control (RBAC)

* Multi-level authentication system.
* Dedicated dashboards for each role.
* Secure authorization architecture.
* Role-specific permissions.

---

## 🏘️ Automated Property Listing Lifecycle

### Standard User Flow

```text
Property Submission
        ↓
Pending Review
        ↓
Admin Verification
        ↓
Marketplace Publication
```

### Verified Agent Flow

```text
Property Submission
        ↓
Auto Approval
        ↓
Instant Marketplace Publication
```

---

## 📬 Inquiry & Communication Engine

* Direct buyer-to-agent communication.
* Real-time inquiry management.
* Context-preserving responses.
* Notification-driven workflows.

---

## 🔄 Global Property Status Synchronization

Property status updates automatically across the entire platform.

Supported states:

* Available
* Reserved
* Sold
* Under Negotiation

Whenever a status changes:

* Property cards update instantly.
* Agent dashboards synchronize.
* Search results refresh automatically.
* Inquiry workflows adapt dynamically.

---

## 📊 Dual-View Agent Dashboard

### Interactive Inquiry Desk

* Priority badges
* Inquiry categorization
* Response management
* Conversation tracking

### Portfolio Management Grid

* Property overview
* Location data
* Pricing metrics
* Listing analytics
* Status management

---

## 🛡️ Administrative Control Portal

* User management
* Role elevation controls
* Property moderation
* Listing approvals
* Record deletion
* System monitoring

---

# 🏗️ System Architecture

```text
Clients
    │
    ▼
Django Views
    │
    ▼
RBAC Authentication Layer
    │
 ┌──┴─────────┐
 ▼            ▼
Agents      Admin
 │            │
 └────┬───────┘
      ▼
Property Management Engine
      ▼
SQLite Database
```

---

# 💻 Technology Stack

## Backend

* Python 3.13
* Django 6.0.1

## Frontend

* HTML5
* CSS3
* Bootstrap 5
* JavaScript

## Database

* SQLite3

## Authentication

* Django Authentication System
* Custom Profile Extension Model

## Development Tools

* Git
* GitHub
* VS Code

---

# 🔬 Technical Highlights

## Django Profile Extension Architecture

* Custom Profile Model
* User Role Separation
* Signal-Based Synchronization

## Relational Database Synchronicity

* Optimized Foreign Keys
* Reverse Relationships
* Related Name References

## Cascading Status Triggers

Property updates automatically propagate throughout the platform.

## Transactional Consistency

* Database Integrity
* M2M Relationship Management
* Atomic Operations

## Portfolio Isolation Matrix

Each agent manages a fully isolated portfolio while remaining synchronized with the marketplace.

---

# 📂 Project Structure

```text
LUX_DWELL/
│
├── accounts/
├── agents/
├── properties/
├── inquiries/
├── dashboard/
├── templates/
├── static/
│   ├── css/
│   ├── js/
│   ├── images/
│
├── media/
├── db.sqlite3
├── manage.py
└── README.md
```

---

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/ashimcs/LUX_DWELL.git
cd LUX_DWELL
```

## Create Virtual Environment

```bash
python -m venv venv
```

## Activate Environment

### Windows

```bash
venv\Scripts\activate
```

### Linux/macOS

```bash
source venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

## Create Admin User

```bash
python manage.py createsuperuser
```

## Run Server

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

---

# 🚀 Future Enhancements

* AI Property Recommendation Engine
* Mortgage Calculator Integration
* Interactive Property Maps
* Online Property Booking
* Digital Contract Signing
* Multi-Agent Teams
* Property Investment Analytics
* Real-Time Chat System
* Payment Gateway Integration

---

# 📸 Screenshots

Add screenshots of:

* Home Page
* Property Listings
* Agent Dashboard
* Admin Dashboard
* Inquiry Desk
* Property Details Page
* Property Submission Form

---

# 👨‍💻 Developer

### Ashim C S

MCA Graduate | Python Developer | Full Stack Developer

GitHub: https://github.com/ashimcs

LinkedIn: https://www.linkedin.com/in/ashim-cs-4b7569397

---

# 📄 License

Licensed under the MIT License.

© 2026 Ashim C S. All Rights Reserved.
