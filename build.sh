#!/bin/bash
set -e  # Exit immediately if any command fails

echo "🔧 Installing dependencies..."
pip install -r requirements.txt

echo "⚡ Running TailwindCSS build..."
python manage.py tailwind build

echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

echo "🛠️ Applying database migrations..."
python manage.py migrate

echo "✅ Build process completed successfully!"
