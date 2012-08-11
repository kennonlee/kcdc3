from classes.models import Event, Location, Registration, Session
from django import forms
from django.contrib import admin
from django.contrib.admin.sites import site
from django.contrib.admin.widgets import ManyToManyRawIdWidget, ForeignKeyRawIdWidget
from django.core.urlresolvers import reverse
from django.utils.encoding import smart_unicode
from django.utils.html import escape
from django.contrib.auth.models import User


# displays registrations as a list in the Event Admin screen
class RegistrationInline(admin.TabularInline):
	model = Registration
	extra = 0
	classes = ('grp-collapse grp-closed',)
	# inline_classes = ('grp-collapse grp-open',)
	fields = ('student', 'date_registered', 'waitlist', 'cancelled', 'date_cancelled', 'attended')
	can_delete = False
	readonly_fields = ('date_registered','date_cancelled')
	raw_id_fields = ['student']
	related_lookup_fields = {
	    'fk': ['student'],
	}

class LocationAdmin(admin.ModelAdmin):
	model = Location

admin.site.register(Location, LocationAdmin)

# lets someone create/edit a Event
class EventAdmin(admin.ModelAdmin):
	fieldsets = [
		(None,			{'fields': ['title', 'slug',('date','type','session'), ('location'), ('status', 'featured',)]}),
		('Teachers/facilitators',	{'fields': [('teachers','facilitators')]}),
		('Description', {
			'classes': ('grp-collapse grp-open',), 
			'fields': [
				'summary', 'description', ('thumbnail', 'main_image'), 
			]
		}),
		('More pre-class details and additional dates', {
			'classes': ('grp-collapse grp-closed',), 
			'fields': [
				'details',
				'additional_dates_text',
			]
		}),
		('Email reminders', {
			'classes': ('grp-collapse grp-closed',), 
			'fields': ['email_welcome_text','email_reminder_text', 'email_reminder', ]
		}),
		('Post-class documentation', {
			'classes': ('grp-collapse grp-closed',), 
			'fields': ['documentation']
		}),
		('Registration',	{'fields': [('max_students', 'registration_status', 'waitlist_status','registration_count','waitlist_count')]}),
	]
	readonly_fields = ('registration_count','waitlist_count')
	prepopulated_fields = {"slug": ("title",)}
	raw_id_fields = ['teachers','facilitators']
	related_lookup_fields = {
	    'm2m': ['teachers', 'facilitators'],
	}
	inlines = (RegistrationInline,)
	class Media:
		js = [
			'tiny_mce/tiny_mce.js',
			'tinymce_setup.js',
		]

	list_display = ('title', 'date','session', 'status','registration_status','max_students', 'registration_count', 'waitlist_count','waitlist_status',)
	list_editable = ('status',)
	list_filter = ('session', 'status', 'registration_status')
	search_fields = ('title',)

admin.site.register(Event, EventAdmin)


# create/edit a Session
class SessionAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, {'fields': [
			'title', 'long_title', 'slug',
			]}),
		('Registration', {'fields': [
			('registration_status', 
			'email_reminder_days')
			]}),
		('Text', {'fields': [
			'description','documentation'
			]}),
	]
	list_display = ('title', 'registration_status')
	prepopulated_fields = {"slug": ("title",)}
	class Media:
		js = [
			'tiny_mce/tiny_mce.js',
			'tinymce_setup.js',
		]

admin.site.register(Session, SessionAdmin)


