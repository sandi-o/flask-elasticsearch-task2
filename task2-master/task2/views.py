#!/usr/bin/python
# -*- coding: utf-8 -*-


import flask
from flask import render_template
from flask import request, redirect, url_for
from task2 import task2
from elasticsearch import Elasticsearch


# instantiate elasticsearch
es = Elasticsearch("http://localhost:9200")


# route to home page
@task2.route('/')
def index():
    return render_template('index.html')


# list of document
@task2.route('/documentlist')
def documentlist():
    # get all documents todo: should be extracted into a method later
    result = es.search(index='', doc_type='', body={"query": {"match_all": {}}})
    return render_template('index.html', result=result, list=list)


# ui for uploading bulk file into elasticsearch (not working)
@task2.route('/bulk')
def bulk():
    return render_template('index.html', bulk=bulk)

# # save each document into elasticsearch
# @task2.route('/save_bulk', methods=['POST'])
# def save_bulk():
#     json_file = request.files['bulk_file']
#     data = open(json_file)
#
#     for each_data in data:
#         return each_data
#     # return


# create document in elasticsearch
@task2.route('/save', methods=['POST'])
def save():
    doc = {'id': request.form['id'],
           'name': request.form['name'],
           'power': request.form['power'],
           'weakness': request.form['weakness']}
    res = es.index(index=request.form['es_index'], doc_type=request.form['es_type'], body=doc)
    # return to index.html.
    return render_template('index.html', result=res['created'])


# remove selected documents in elasticsearch
@task2.route('/remove', methods=['GET', 'POST'])
def remove():
    # delete by index from earlier research
    # res = es.indices.delete(index='test-index', ignore=[400, 404])
    # delete by document data_shard[0] = index , data_shard[1] = doc_type, data_shard[2] = id
    data = request.form.getlist('data[]')
    for each_data in data:
        data_shard = each_data.split('~')
        es.delete(index=data_shard[1], doc_type=data_shard[2], id=data_shard[0], ignore=[400, 404])

    # return to index.html.
    return redirect(url_for('documentlist'))


# update selected documents in elasticsearch
@task2.route('/update', methods=['GET', 'POST'])
def edit():
    # from dialog request fields
    body = {"doc": {'id': request.form['id'], 'name': request.form['name'], 'power': request.form['power'], 'weakness': request.form['weakness']}}
    # update by document data_shard[0] = index , data_shard[1] = doc_type, data_shard[2] = id
    data = request.form.getlist('checkboxes')
    for each_data in data:
        data_shard = each_data.split('~')
        es.update(index=data_shard[1], doc_type=data_shard[2], id=data_shard[0], body=body)

    # return to index.html.
    return redirect(url_for('documentlist'))
