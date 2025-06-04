# VeriPharm

VeriPharm is a Django-based web application designed to trace drugs and detect potential drug abuse. This project provides transparency across the pharmaceutical supply chain and allows consumers to verify the authenticity of drugs using QR codes.

## 🔧 Features to be implemented 
- Drug traceability from manufacturer to consumer
- One-time QR code verification system
- User roles: Admin, Manufacturer, Distributor, Pharmacist, Consumer
- Drug authenticity validation system

## 🚀 Getting Started

Follow these steps to set up the project on your local machine.

### 1. Clone the Repository

```bash
git clone https://github.com/Mhaxe/VeriPharm.git
cd VeriPharm
````

### 2. Set Up a Virtual Environment (Optional but Recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply Migrations

```bash
python manage.py migrate
```

### 5. Create a Superuser (For Admin Access)

```bash
python manage.py createsuperuser
```

Follow the prompts to set up your admin credentials.

### 6. Run the Development Server

```bash
python manage.py runserver
```

Now open your browser and go to:
[http://127.0.0.1:8000](http://127.0.0.1:8000)

## 🗂 Project Structure

```
VeriPharm/
├── manage.py
├── app_name/         # Your main Django app
├── VeriPharm/        # Project settings
└── templates/        # HTML Templates
```

## 🛠 Tech Stack

* Python
* Django
* SQLite (default, changeable)
* Bootstrap (for UI)
* QR Code integration
