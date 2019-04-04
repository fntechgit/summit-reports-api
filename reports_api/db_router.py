"""
 * Copyright 2019 OpenStack Foundation
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 * http://www.apache.org/licenses/LICENSE-2.0
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
"""


class DBRouter(object):
    """
    A router to control all database operations on models in the
    reports application.
    """
    def db_for_read(self, model, **hints):
        """
        Attempts to read reports models go to openstack_db.
        """
        if model._meta.app_label == 'reports':
            return 'openstack_db'
        return 'default'

    def db_for_write(self, model, **hints):
        """
        Attempts to write reports models go to openstack_db.
        """
        if model._meta.app_label == 'reports':
            return None
        return 'default'

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        All non-auth models end up in this pool.
        """

        if app_label == 'reports':
            return False
        return None