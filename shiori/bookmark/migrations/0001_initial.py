# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Category'
        db.create_table('category', (
            ('id', self.gf('shortuuidfield.fields.ShortUUIDField')(max_length=22, primary_key=True)),
            ('category', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal(u'bookmark', ['Category'])

        # Adding model 'Tag'
        db.create_table('tag', (
            ('id', self.gf('shortuuidfield.fields.ShortUUIDField')(max_length=22, primary_key=True)),
            ('tag', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal(u'bookmark', ['Tag'])

        # Adding model 'Bookmark'
        db.create_table('bookmark', (
            ('id', self.gf('shortuuidfield.fields.ShortUUIDField')(max_length=22, primary_key=True)),
            ('url', self.gf('django.db.models.fields.URLField')(unique=True, max_length=200)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bookmark.Category'])),
            ('registered_datetime', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('is_hide', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'bookmark', ['Bookmark'])

        # Adding model 'BookmarkTag'
        db.create_table('bookmark_tag', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('bookmark', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bookmark.Bookmark'], db_column='bookmark_id')),
            ('tag', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bookmark.Tag'], db_column='tag_id')),
        ))
        db.send_create_signal(u'bookmark', ['BookmarkTag'])

        # Adding unique constraint on 'BookmarkTag', fields ['bookmark', 'tag']
        db.create_unique('bookmark_tag', ['bookmark_id', 'tag_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'BookmarkTag', fields ['bookmark', 'tag']
        db.delete_unique('bookmark_tag', ['bookmark_id', 'tag_id'])

        # Deleting model 'Category'
        db.delete_table('category')

        # Deleting model 'Tag'
        db.delete_table('tag')

        # Deleting model 'Bookmark'
        db.delete_table('bookmark')

        # Deleting model 'BookmarkTag'
        db.delete_table('bookmark_tag')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'bookmark.bookmark': {
            'Meta': {'object_name': 'Bookmark', 'db_table': "'bookmark'"},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bookmark.Category']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('shortuuidfield.fields.ShortUUIDField', [], {'max_length': '22', 'primary_key': 'True'}),
            'is_hide': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'registered_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['bookmark.Tag']", 'through': u"orm['bookmark.BookmarkTag']", 'symmetrical': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '200'})
        },
        u'bookmark.bookmarktag': {
            'Meta': {'unique_together': "(('bookmark', 'tag'),)", 'object_name': 'BookmarkTag', 'db_table': "'bookmark_tag'"},
            'bookmark': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bookmark.Bookmark']", 'db_column': "'bookmark_id'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bookmark.Tag']", 'db_column': "'tag_id'"})
        },
        u'bookmark.category': {
            'Meta': {'object_name': 'Category', 'db_table': "'category'"},
            'category': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'id': ('shortuuidfield.fields.ShortUUIDField', [], {'max_length': '22', 'primary_key': 'True'})
        },
        u'bookmark.tag': {
            'Meta': {'object_name': 'Tag', 'db_table': "'tag'"},
            'id': ('shortuuidfield.fields.ShortUUIDField', [], {'max_length': '22', 'primary_key': 'True'}),
            'tag': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['bookmark']
