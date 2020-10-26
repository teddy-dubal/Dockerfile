#!/usr/bin/env/python
# -*- coding: utf-8 -*-
#
# (c) 2016 WebDevOps.io
#
# This file is part of Dockerfile Repository.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and
# to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions
# of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS
# OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import os, subprocess, tempfile,random,string
from .DockerBaseClient import DockerBaseClient
from webdevops import Command

class DockerCliClient(DockerBaseClient):

    def uniqid(length):
        letters = string.ascii_letters
        result_str = ''.join(random.choice(letters) for i in range(length))
        return result_str

    def pull_image(self, name, tag):
        """
        Build dockerfile
        """
        cmd = ['docker', 'pull', '%s:%s' % (name, tag)]
        return Command.execute(cmd)

    def build_dockerfile(self, path, name, nocache=False):
        """
        Build dockerfile
        """
        print self.uniqid()
        instanceName = name.replace('/','-').replace(':','-')+ "_" +self.uniqid(8) 
        cmdBuilderInstance = ['docker','buildx', 'create','--name',instanceName]
        Command.execute(cmdBuilderInstance)

        cmdBuilderInstanceUse = ['docker','buildx', 'use',instanceName]
        Command.execute(cmdBuilderInstanceUse)
        
        cmd = ['docker','buildx', 'build','--platform', 'linux/arm64,linux/arm/v7','--tag', name, os.path.dirname(path)]

        if nocache:
            cmd.append('--no-cache')

        return Command.execute(cmd)

    def push_image(self, name):
        """
        Push one Docker image to registry
        """
        cmd = ['docker', 'push', name]
        return Command.execute(cmd)
