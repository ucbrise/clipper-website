from flask import Flask, json
from flask_restplus import Resource, Api, fields, Namespace

import descriptions

app = Flask(__name__)
app.config['RESTPLUS_MASK_SWAGGER'] = False
api = Api(
    app,
    title=descriptions.api['title'],
    description=descriptions.api['description'],
    default='admin_addr',
    default_label='Admin Address',
    version='0.3.0')
query = api.namespace('query_addr')

application_fields = api.model(
    'Application', {
        "name":
        fields.String(
            required=True,
            description=descriptions.app['name'],
            example='simple-app'),
        "input_type":
        fields.String(
            required=True,
            example='doubles',
            enum=["integers", "floats", "doubles", "bytes", "strings"],
            description=descriptions.app['input_type']),
        "default_output":
        fields.String(
            required=True,
            example='[42.0]',
            description=descriptions.app['default_output']),
        "latency_slo_micros":
        fields.Integer(
            required=True,
            example=100000,
            description=descriptions.app['latency_slo_micros'])
    })

model_version_fileds = api.model(
    'Model Version', {
        'model_name':
        fields.String(
            required=True,
            example='sum_model',
            description='The name of the model'),
        'model_version':
        fields.String(
            required=True,
            example='1',
            description=descriptions.misc['model_version'])
    })

app_model_link_fields = api.model(
    'Link', {
        "app_name":
        fields.String(
            required=True,
            example='sum-application',
            description='The name of the application'),
        "model_names":
        fields.List(
            fields.String(),
            required=True,
            example=['basic-sum-1'],
            description=
            'List of  The name of the model to link to the application')
    })

model_fields = api.model(
    'Model', {
        "model_name":
        fields.String(
            required=True,
            example='sum-model',
            description=descriptions.model['name']),
        "model_version":
        fields.String(
            required=True,
            example='1',
            description=descriptions.model['version']),
        "labels":
        fields.List(
            fields.String(),
            example=["Team: DevOps"],
            description=descriptions.model['labels']),
        "input_type":
        fields.String(
            required=True,
            enum=["integers", "floats", "doubles", "bytes", "strings"],
            example="doubles",
            description=descriptions.model['input_type']),
        "container_name":
        fields.String(
            required=True,
            example='clipper/example-container',
            description=descriptions.model['image']),
        "batch_size":
        fields.Integer(
            required=True,
            example=10,
            description=descriptions.model['batch_size'])
    })

verbose_field = api.model(
    'Verbosity', {
        'verbose':
        fields.Boolean(
            required=True, 
            description=descriptions.misc['boolean'],
            example='true')
    })

name_field = api.model(
    'Name', {
        'name':
        fields.String(
            required=True,
            example='simple-example',
            description='Exact name of app')
    })

app_name_field = api.model(
    'App Name', {
        'app_name':
        fields.String(
            required=True,
            example='simple-example',
            description='Exact name of app')
    })

replica_field = api.model(
    'Model Container', {
        'input_type':
        fields.String(
            example='doubles',
            enum=["integers", "floats", "doubles", "bytes", "strings"],
            description=descriptions.model['input_type']),
        'model_id':
        fields.String(
            required=True,
            example='simple-example:1',
            description="Automatically assigned model id"),
        'model_name':
        fields.String(
            required=True,
            example='simple-example',
            description=descriptions.model['name']),
        'model_replica_id':
        fields.Integer(
            example=1, description='Automatically Assgined Replica ID'),
        'model_version':
        fields.String(
            required=True,
            example='1',
            description=descriptions.model['version'])
    })

input_field = query.model(
    'Query Input', {
        'input [OR]': fields.List(fields.Raw(
                        example=2.3), description='The query input as single string OR list of primitive.', required=True),
        'input_batch': fields.List(fields.List(fields.Raw(
                        example=2.3), description='The query input as list of string OR 2d list of primitive.', required=True)),
    }
)

query_response_field = query.model(
    'Query Result', {
        'default': fields.Boolean(
            example='true',
            description='Whether or not this result is default response. The reason for default is given in the default_explanation field.'
        ), 
        'output': fields.Raw(
            example=2.2,
            description='The prediction output.'
        ),
        'query_id': fields.Integer(
            example=42,
            description='The query id by application'
        ),
        'default_explanation': fields.String(
            example="Failed to retrieve a prediction response within the specified latency SLO",
            description='Explanation for returning the default response. This field is only present when default is true.'
        )
    }
)


@api.route('/dump')
@api.hide
class Dump(Resource):
    def get(self):
        with open('swagger.json', 'w') as f:
            json.dump(api.__schema__, f)
        return api.__schema__


@api.route('/admin/add_app')
class AddApplication(Resource):
    @api.expect(application_fields)
    @api.response(200, 'OK')
    @api.response(400, 'Bad Request')
    def post(self):
        """add_app

        Register a new application with Clipper.

        An application in Clipper corresponds to a named REST endpoint that can be used to request
        predictions. This command will attempt to create a new endpoint with the provided name.
        Application names must be unique. This command will fail if an application with the provided
        name already exists.
        """
        pass


@api.route('/admin/set_model_version')
class SetModelVersion(Resource):
    @api.expect(model_version_fileds)
    @api.response(200, 'OK')
    @api.response(400, 'Bad Request')
    def post(self):
        """set_model_version
        

        Changes the current model version to "model_version".

        This method can be used to perform model roll-back and roll-forward. The
        version can be set to any previously deployed version of the model.

        Note:

        Model versions automatically get updated when
        `clipper_admin.ClipperConnection.deploy_model()` is called. There is no need to
        manually update the version after deploying a new model.
        """
        pass


@api.route('/admin/add_model_links')
class AddModelLinks(Resource):
    @api.expect(app_model_link_fields)
    @api.response(200, 'OK')
    @api.response(400, 'Bad Request')
    def post(self):
        """add_model_links

        Routes requests from the specified app to be evaluted by the specified model.

        Note:

        Both the specified model and application must be registered with Clipper, and they
        must have the same input type. If the application has previously been linked to a different
        model, this command will fail.
        """
        pass


@api.route('/admin/add_model')
class AddModel(Resource):
    @api.expect(model_fields)
    @api.response(200, 'OK')
    @api.response(400, 'Bad Request')
    def post(self):
        """add_model

        Registers a new model version with Clipper.

        This method does not launch any model containers, it only registers the model description
        (metadata such as name, version, and input type) with Clipper. A model must be registered
        with Clipper before it can be linked to an application.

        You should rarely have to use this method directly. Using one the Clipper deployer
        methods in `clipper_admin.deployers` or calling ``build_and_deploy_model`` or
        ``deploy_model`` will automatically register your model with Clipper.
        """
        pass


@api.route('/admin/get_all_applications')
class GetAllApp(Resource):
    @api.expect(verbose_field)
    @api.marshal_list_with(application_fields)
    @api.response(400, 'Bad Request')
    def post(self):
        """get_all_applications

        Gets information about all applications registered with Clipper.
        
        If 'verbose' is set to False, the returned list contains the apps' names; 
        if 'verbose' set to True, the list contains application info dictionaries.
        These dictionaries have the same attribute name-value pairs that were
        provided to `clipper_admin.ClipperConnection.register_application`.

        Returns a list of information about all apps registered to Clipper.
        If no apps are registered with Clipper, an empty list is returned.
        """
        pass


@api.route('/admin/get_application')
class GetApp(Resource):
    @api.expect(name_field)
    @api.marshal_with(application_fields)
    @api.response(400, 'Bad Request')
    def post(self):
        """get_application

        Gets detailed information about a registered application.
        
        'name' parameter is the name of the application to look up.

        Returns a dictionary with the specified application's info. This
        will contain the attribute name-value pairs that were provided to
        `clipper_admin.ClipperConnection.register_application`.
        If no application with name ``name`` is
        registered with Clipper, None is returned.
        """
        pass


@api.route('/admin/get_linked_models')
class GetLinkedModel(Resource):
    @api.expect(app_name_field)
    @api.marshal_list_with(fields.String(example="Model Name"))
    @api.response(400, 'Bad Request')
    def post(self):
        """get_linked_models

        Retrieves the models linked to the specified application.

        'app_name' parameter is the name of the application

        Returns a list of the names of models linked to the app.
        If no models are linked to the specified app, None is returned.
        """
        pass


@api.route('/admin/get_all_models')
class GetAppModel(Resource):
    @api.expect(verbose_field)
    @api.marshal_list_with(model_fields)
    @api.response(400, 'Bad Request')
    def post(self):
        """get_all_models

        Gets information about all models registered with Clipper.

        If 'verbose' is set to False, the returned list contains the models' names.
        If 'verbose' set to True, the list contains model info dictionaries.

        Returns a list of information about all apps registered to Clipper.
        If no models are registered with Clipper, an empty list is returned.
        """
        pass


@api.route('/admin/get_model')
class GetModel(Resource):
    @api.expect(model_version_fileds)
    @api.marshal_with(model_fields)
    @api.response(400, 'Bad Request')
    def post(self):
        """get_model

        Gets detailed information about a registered model.

        'model_name' is the name of the model to look up

        'model_version' is the version of the model to look up

        Returns a dictionary with the specified model's info.
        If no model with name `model_name@model_version` is
        registered with Clipper, None is returned.
        """
        pass


@api.route('/admin/get_all_containers')
class GetAllContainers(Resource):
    @api.expect(verbose_field)
    @api.marshal_list_with(replica_field)
    @api.response(400, 'Bad Request')
    def post(self):
        """get_all_containers
        
        Gets information about all model containers registered with Clipper.

        If 'verbose' is set to False, the returned list contains the apps' names.
        If 'verbose' is set to True, the list contains container info dictionaries.

        Returns a list of information about all model containers known to Clipper.
        If no containers are registered with Clipper, an empty list is returned.
        """
        pass


@api.route('/admin/get_container')
class GetContainer(Resource):
    @api.expect(replica_field)
    @api.marshal_with(replica_field)
    @api.response(400, 'Bad Request')
    def post(self):
        """get_container

        Gets detailed information about a registered container.

        'name' is the name of the container to look up

        'version' is the version of the container to look up

        'replica_id' is the container replica to look up

        Returns a dictionary with the specified container's info.
        If no corresponding container is registered with Clipper, None is returned.
        """
        pass



@query.route('/<string:application_name>/predict')
@query.param('application_name', 'The name of appplication to query.')
class Prediect(Resource):
    @query.expect(input_field)
    @query.marshal_with(query_response_field)
    @query.response(400, 'Bad Request')
    def post(self):
        """predict

        Submit a new query to application. The application name needs to specified in 
        the path; and data needs to be submitted via a POST JSON request. 

        Response will contains either the data returned by model or the default response. 
        This can be distinguished by the default field.
        If the default field is True, there will be another field present called "default_explanation" 
        whose value is a string describing the reason that a default response was returned. 
        This field is not present if default is False.

        Starting 0.3.0, we also have batch prediction interface, see more at: http://clipper.ai/tutorials
        """
        pass


if __name__ == '__main__':
    app.run(debug=True, threaded=True)
