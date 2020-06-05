#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# flask manager
#
# 20-3-30 leo : Init

import os
from app import create_app, db
from flask_migrate import Migrate

app = create_app(os.getenv('FLASK_ENV') or 'default')
migrate = Migrate(app, db)


@app.cli.command('deploy')
def deploy():
    db.create_tables(app)
    print('deploy success.')



