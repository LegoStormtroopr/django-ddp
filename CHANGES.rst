Change Log
==========

0.12.1
------
* Add `AleaIdMixin` which provides `aid = AleaIdField(unique=True)` to 
  models.
* Use `AleaIdField(unique=True)` wherever possible when translating 
  between Meteor style identifiers and Django primary keys, reducing 
  round trips to the database and hence drastically improving 
  performance when such fields are available.

0.12.0
------
* Get path to `star.json` from view config (defined in your urls.py) 
  instead of from settings.
* Dropped `dddp.server.views`, use `dddp.views` instead.

0.11.0
------
* Support more than 8KB of change data by splitting large payloads into 
  multiple chunks.

0.10.2
------
* Add `Logs` publication that can be configured to emit logs via DDP 
  through the use of the `dddp.logging.DDPHandler` log handler.
* Add option to dddp daemon to provide a BackdoorServer (telnet) for 
  interactive debugging (REPL) at runtime.

0.10.1
------
* Bugfix dddp.accounts forgot_password feature.

0.10.0
------
* Stop processing request middleware upon connection - see
  https://github.com/commoncode/django-ddp/commit/e7b38b89db5c4e252ac37566f626b5e9e1651a29 
  for rationale.  Access to `this.request.user` is gone.
* Add `this.user` handling to dddp.accounts.

0.9.14
------
* Fix ordering of user added vs login ready in dddp.accounts 
  authentication methods.

0.9.13
------
* Add dddp.models.get_object_ids helper function.
* Add ObjectMappingMixini abstract model mixin providing
  GenericRelation back to ObjectMapping model.

0.9.12
------
* Bugfix /app.model/schema helper method on collections to work with 
  more model field types.

0.9.11
------
* Fix bug in post login/logout subscription handling.

0.9.10
------
* Fix bug in Accounts.forgotPassword implementation.

0.9.9
-----
* Match return values for Accounts.changePassword and 
  Accounts.changePassword methods in dddp.accounts submodule.

0.9.8
-----
* Fix method signature for Accouts.changePassword.

0.9.7
-----
* Updated Accounts hashing to prevent cross-purposing auth tokens.

0.9.6
-----
* Correct method signature to match Meteor Accounts.resetPassword in 
  dddp.accounts submodule.

0.9.5
-----
* Include array of `permissions` on User publication.

0.9.4
-----
* Use mimetypes module to correctly guess mime types for Meteor files 
  being served.

0.9.3
-----
* Include ROOT_URL_PATH_PREFIX in ROOT_URL when serving Meteor build 
  files.

0.9.2
-----
* Use HTTPS for DDP URL if settings.SECURE_SSL_REDIRECT is set.

0.9.1
-----
* Added support for django.contrib.postres.fields.ArrayField 
  serialization.

0.9.0
-----
* Added Django 1.8 compatibility.  The current implementation has a
  hackish (but functional) implementation to use PostgreSQL's
  `array_agg` function.  Pull requests are welcome.
* Retained compatibility with Django 1.7, though we still depend on the
  `dbarray` package for this even though not strictly required with
  Django 1.8.  Once again, pull requests are welcome.

0.8.1
-----
* Add missing dependency on `pybars3` used to render boilerplate HTML
  template when serving Meteor application files.

0.8.0
-----
* Add `dddp.server` Django app to serve Meteor application files.
* Show input params after traceback if exception occurs in API methods.
* Small pylint cleanups.

0.7.0
-----
* Refactor serialization to improve performance through reduced number
  of database queries, especially on sub/unsub.
* Fix login/logout user subscription, now emitting user `added`/
  `removed` upon `login`/`logout` respectively.

0.6.5
-----
* Use OrderedDict for geventwebsocket.Resource spec to support
  geventwebsockets 0.9.4 and above.

0.6.4
-----
* Send `removed` messages when client unsubscribes from publications.
* Add support for SSL options and --settings=SETTINGS args in dddp tool.
* Add `optional` and `label` attributes to ManyToManyField simple
  schema.
* Check order of added/changed when emitting WebSocket frames rather
  than when queuing messages.
* Move test projects into path that can be imported post install.

0.6.3
-----
* Refactor pub/sub functionality to fix support for `removed` messages.

0.6.2
-----
* Bugfix issue where DDP connection thread stops sending messages after
  changing item that has subscribers for other connections but not self.

0.6.1
-----
* Fix `createUser` method to login new user after creation.
* Dump stack trace to console on error for easier debugging DDP apps.
* Fix handing of F expressions in object change handler.
* Send `nosub` in response to invalid subscription request.
* Per connection tracking of sent objects so changed/added sent
  appropriately.

0.6.0
-----
* Add dddp.accounts module which provides password based auth mapping to
  django.contrib.auth module.
* Fix ordering of change messages and result message in method calls.

0.5.0
-----
* Drop relations to sessions.Session as WebSocket requests don't have
  HTTP cookie support -- **you must `migrate` your database after
  upgrading**.
* Refactor core to support custom serialization per collection, and
  correctly dispatch change messages per collection.
* Allow specifying specific collection for publication queries rather
  than assuming the auto-named default collections.
* Improve schema introspection to include options for fields with
  choices.
* Cleanup transaction handling to apply once at the entry point for DDP
  API calls.

0.4.0
-----
* Make live updates honour user_rel restrictions, also allow superusers
  to see everything.
* Support serializing objects that are saved with F expressions by
  reading field values for F expressions from database explicitly before
  serializing.
* Allow `fresh` connections from browsers that have not established a
  session in the database yet, also allow subscriptions from
  unauthenticated sessions (but don't show any data for collections that
  have user_rel items defined).  This change includes a schema change,
  remember to run migrations after updating.

0.3.0
-----
* New DB field: Connection.server_addr -- **you must `migrate` your
  database after upgrading**.
* Cleanup connections on shutdown (and purge associated subscriptions).
* Make `dddp` management command a subclass of the `runserver` command
  so that `staticfiles` work as expected.
* Fix non-threadsafe failure in serializer - now using thread local
  serializer instance.
* Fix `unsubscribe` from publications.
* Fix `/schema` method call.

0.2.5
-----
* Fix foreign key references in change messages to correctly reference
  related object rather than source object.

0.2.4
-----
* Fix unicode rendering bug in DDP admin for ObjectMapping model.

0.2.3
-----
* Add `dddp` console script to start DDP service in more robust manner than using the dddp Django mangement command.
