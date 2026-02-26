#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'telusko.settings')
django.setup()

from travello.models import Contact

def view_contacts():
    """Simple script to view contact form submissions"""
    contacts = Contact.objects.all().order_by('-created_at')
    
    print(f"\n{'='*80}")
    print(f"CONTACT FORM SUBMISSIONS ({contacts.count()} total)")
    print(f"{'='*80}")
    
    for contact in contacts:
        print(f"\nID: {contact.id}")
        print(f"Name: {contact.name}")
        print(f"Email: {contact.email}")
        print(f"Subject: {contact.subject}")
        print(f"Message: {contact.message}")
        print(f"Created: {contact.created_at}")
        print(f"{'-'*40}")
    
    if not contacts:
        print("No contact submissions found.")

if __name__ == "__main__":
    view_contacts()