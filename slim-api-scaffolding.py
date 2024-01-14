"""
Slim API Scaffolding Script

Generates a basic directory and code file structure to kickstart the development of a Slim API,
adhering to the Repositories design architecture in conjunction with MVC design principles.

Author: Silvano Emanuel Roqués
License: GNU General Public License v3.0
Contributions Welcome: Feel free to contribute! Open an issue or submit a pull request on GitHub.
GitHub Repository: https://github.com/sjlvanq/slim-api-scaffolding

GNU General Public License v3.0

Copyright (c) 2024, Silvano Emanuel Roqués

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see https://www.gnu.org/licenses/.
"""

import os
from jinja2 import Template
from inflection import pluralize
from argparse import ArgumentParser, RawTextHelpFormatter

class EntityNameVariations:
    def __init__(self,name):
        self.lowercase = name.lower()
        self.capitalized = name.capitalize()
        self.lowercase_pl = pluralize(self.lowercase)
        self.capitalized_pl = pluralize(self.capitalized)

def get_model_methods(entity_name):
    return {
    f"get{entity_name.capitalized_pl}": {
        "description": f"Retrieve all {entity_name.lowercase_pl}.",
        "params": [],
        "return_type": "array",
        "return_desc": f"Array of {entity_name.lowercase_pl}.",
    },
    f"get{entity_name.capitalized}ById": {
        "description": f"Retrieve a specific {entity_name.lowercase} by its ID.",
        "params": [("id", "int", f"ID of the {entity_name.lowercase}")],
        "return_type": "array|null",
        "return_desc": f"Data of the {entity_name.lowercase} or null if not found.",
    },
    f"add{entity_name.capitalized}": {
        "description": f"Create a new {entity_name.lowercase}.",
        "params": [("data", "array", f"Data for the new {entity_name.lowercase}")],
        "return_type": "int|false",
        "return_desc": "ID of the new record or false in case of error.",
    },
    f"update{entity_name.capitalized}": {
        "description": f"Modify an existing {entity_name.lowercase} by its ID.",
        "params": [
            ("id", "int", f"The ID of the {entity_name.lowercase} to update"),
            ("data", "array", f"New data of the {entity_name.lowercase}")
        ],
        "return_type": "bool",
        "return_desc": "True on success, false on failure.",
    },
    f"delete{entity_name.capitalized}": {
        "description": f"Remove a specific {entity_name.lowercase} by its ID.",
        "params": [("id", "int", f"The ID of the {entity_name.lowercase} to delete")],
        "return_type": "bool",
        "return_desc": "True on success, false on failure.",
    }
    }

def get_controller_methods(entity_name):
    return {
    f"getAll{entity_name.capitalized_pl}": {
        "description": f"Retrieve all {entity_name.lowercase_pl}.",
        "params": [
            ("request", "Request", "The HTTP request object."),
            ("response", "Response", "The HTTP response object.")
        ],
        "return_type": "Response",
        "return_desc": "The HTTP response",
        "body": f"""
        ${ entity_name.lowercase_pl } = $this->{ entity_name.lowercase }Repository->getAll();
        return $response->withJson(${ entity_name.lowercase_pl });
        """
    },
    f"get{entity_name.capitalized}ById": {
        "description": f"Retrieve a specific {entity_name.lowercase} by its ID.",
        "params": [
            ("request", "Request", "The HTTP request object."),
            ("response", "Response", "The HTTP response object."),
            ("args", "array", "The route parameters.")
        ],
        "return_type": "Response",
        "return_desc": "The HTTP response.",
        "body": f"""
        ${entity_name.lowercase}Id = (int)$args["id"];
        ${entity_name.lowercase} = $this->{entity_name.lowercase}Repository->getById(${entity_name.lowercase}Id);

        if (${entity_name.lowercase}) {{
            return $response->withJson(${entity_name.lowercase});
        }} else {{
            return $response->withStatus(404)->withJson(["error" => "{entity_name.capitalized} not found"]);
        }}
        """
    },
    f"create{entity_name.capitalized}": {
        "description": f"Create a new {entity_name.lowercase}.",
        "params": [
            ("request", "Request", "The HTTP request object."),
            ("response", "Response", "The HTTP response object.")
        ],
        "return_type": "Response",
        "return_desc": "The HTTP response.",
        "body": f"""
        $data = $request->getParsedBody();
        $result = $this->{entity_name.lowercase}Repository->create($data);

        if ($result !== false) {{
            return $response->withJson(['id' => $result]);
        }} else {{
            return $response->withStatus(500)->withJson(['error' => 'Failed to create {entity_name.lowercase}']);
        }}
        """
    },
    f"update{entity_name.capitalized}": {
        "description": f"Modify an existing {entity_name.lowercase} by its ID.",
        "params": [
            ("request", "Request", "The HTTP request object."),
            ("response", "Response", "The HTTP response object."),
            ("args", "array", "The route parameters.")
        ],
        "return_type": "Response",
        "return_desc": "The HTTP response.",
        "body": f"""
        ${entity_name.lowercase}Id = (int)$args['id'];
        $data = $request->getParsedBody();
        $result = $this->{entity_name.lowercase}Repository->update(${entity_name.lowercase}Id, $data);

        if ($result) {{
            return $response->withJson(['success' => true]);
        }} else {{
            return $response->withStatus(500)->withJson(['error' => 'Failed to update {entity_name.lowercase}']);
        }}
        """
    },
    f"delete{entity_name.capitalized}": {
        "description": f"Delete a specific {entity_name.lowercase} by its ID.",
        "params": [
            ("request", "Request", "The HTTP request object."),
            ("response", "Response", "The HTTP response object."),
            ("args", "array", "The route parameters.")
        ],
        "return_type": "Response",
        "return_desc": "The HTTP response.",
        "body": f"""
        ${entity_name.lowercase}Id = (int)$args['id'];
        $result = $this->{entity_name.lowercase}Repository->delete(${entity_name.lowercase}Id);

        if ($result) {{
            return $response->withJson(['success' => true]);
        }} else {{
            return $response->withStatus(500)->withJson(['error' => 'Failed to delete {entity_name.lowercase}']);
        }}
        """
    },
    }

def get_repository_interface_methods(entity_name):
    return {
    "getAll": {
        "description": f"Gets all {entity_name.lowercase_pl}.",
        "return_type": "array|null",
        "return_desc": f"Array of {entity_name.lowercase_pl} or null.",
    },
    "getById": {
        "description": f"Retrieve a specific {entity_name.lowercase} by its ID.",
        "params": [("id", "int", f"ID of the {entity_name.lowercase}")],
        "return_type": "array|null",
        "return_desc": f"Data of the {entity_name.lowercase} or null if not found.",
    },
    "create": {
        "description": f"Creates a new {entity_name.lowercase}.",
        "params": [("data", "array", f"Data of the new {entity_name.lowercase}")],
        "return_type": "int|false",
        "return_desc": "ID of the new record or false in case of error.",
    },
    "update": {
        "description": f"Updates an existing {entity_name.lowercase} by its ID.",
        "params": [
            ("id", "int", f"ID of the {entity_name.lowercase} to update"),
            ("data", "array", f"New data of the {entity_name.lowercase}")
        ],
        "return_type": "bool",
        "return_desc": "True on success, false on failure.",
    },
    "delete": {
        "description": f"Deletes a specific {entity_name.lowercase} by its ID.",
        "params": [("id", "int", f"ID of the {entity_name.lowercase} to delete")],
        "return_type": "bool",
        "return_desc": "True on success, false on failure.",
    },
    }

def get_repository_methods(entity_name):
    return {
    "getAll": {
        "description": f"Retrieve all {entity_name.lowercase_pl}.",
        "params": [],
        "return": "array|null",
        "return_desc": f"Array of {entity_name.lowercase_pl} or null.",
    },
    "getById": {
        "description": f"Retrieve a specific {entity_name.lowercase} by its ID.",
        "params": [("id", "int", f"ID of the {entity_name.lowercase}")],
        "return": "array|null",
        "return_desc": f"Data of the {entity_name.lowercase} or null if not found.",
    },
    "create": {
        "description": f"Create a new {entity_name.lowercase}.",
        "params": [("data", "array", f"Data for the new {entity_name.lowercase}")],
        "return": "int|false",
        "return_desc": "ID of the new record or false in case of error.",
    },
    "update": {
        "description": f"Modify an existing {entity_name.lowercase} by its ID.",
        "params": [
            ("id", "int", f"The ID of the {entity_name.lowercase} to update"),
            ("data", "array", f"New data of the {entity_name.lowercase}")
        ],
        "return": "bool",
        "return_desc": "True on success, false on failure.",
    },
    "delete": {
        "description": f"Delete a specific {entity_name.lowercase} by its ID.",
        "params": [("id", "int", f"The ID of the {entity_name.lowercase} to delete")],
        "return": "bool",
        "return_desc": "True on success, false on failure.",
    }
    }

def get_routes_methods(entity_name):
    return {
    "getAll": {
        "endpoint": "",
        "req_method": "GET",
        "controller_method": f"getAll{entity_name.capitalized_pl}",
        "description": f"Retrieve all {entity_name.lowercase_pl}.",
        "request_params": [],
    },
    "getById": {
        "endpoint": "/{id}",
        "req_method": "GET",
        "controller_method": f"get{ entity_name.capitalized }ById",
        "description": f"Retrieve a specific {entity_name.lowercase} by its ID.",
        "request_params": [],
    },
    "create": {
        "endpoint": "",
        "req_method": "POST",
        "controller_method": f"create{ entity_name.capitalized }",
        "description": f"Create a new {entity_name.lowercase}.",
        "request_params": [],
    },
    "update": {
        "endpoint": "/{id}",
        "req_method": "PUT",
        "controller_method": f"update{ entity_name.capitalized }",
        "description": f"Modify an existing {entity_name.lowercase} by its ID.",
        "request_params": [],
    },
    "delete": {
        "endpoint": "/{id}",
        "req_method": "DELETE",
        "controller_method": f"delete{ entity_name.capitalized }",
        "description": f"Delete a specific {entity_name.lowercase} by its ID.",
        "request_params": [],
    },
    }

template_model = r"""
<?php

namespace App\Models;

/**
 * Clase {{ entity_name }}Model
 *
 * Represents the model of {{ entity_name | lower }} in the database.
 *
 * @package App\Models
 */
class {{ entity_name }}Model
{
    {% for method_name, method_data in methods.items() %}
    /**
     * {{ method_data['description'] }}
     *
     {% for param_name, param_type, param_description in method_data['params'] -%}
     * @param {{ param_type }} ${{ param_name }} - {{ param_description }}
     {% endfor -%}
     * @return {{ method_data['return_type'] }} - {{ method_data['return_desc'] }}
     */
    public function {{ method_name }}({% for param_name, param_type, _ in method_data['params'] %}{{ param_type }} ${{ param_name }}{% if not loop.last %}, {% endif %}{% endfor %})
    {
        // Logic for {{ method_data['description']|lower }}
    }
    {% endfor %}
}
"""

template_controller = r"""
<?php

namespace App\Controllers;

use Psr\Http\Message\ResponseInterface as Response;
use Psr\Http\Message\ServerRequestInterface as Request;
use App\Repositories\{{ entity_name }}RepositoryInterface;

/**
 * Class {{ entity_name }}Controller
 *
 * Controller to manage requests related to {{ entities_name | lower }}.
 *
 * @package App\Controllers
 */
class {{ entity_name }}
{
    /**
     * @var {{ entity_name }}RepositoryInterface {{ entity_name }} repository.
     */
    protected ${{ entities_name | lower }}Repository;

    /**
     * {{ entity_name }}Controller constructor.
     *
     * @param {{ entity_name }}RepositoryInterface ${{ entity_name | lower }}Repository  {{ entity_name }} repository to use.
     */
    public function __construct({{ entity_name }}RepositoryInterface ${{ entity_name | lower }}Repository)
    {
        $this->{{ entity_name | lower }}Repository = ${{ entity_name | lower }}Repository;
    }
    {% for method_name, method_data in methods.items() %}
    /**
     * {{ method_data['description'] }}
     *
     {% for param_name, param_type, param_description in method_data['params'] -%}
     * @param {{ param_type }} ${{ param_name }} - {{ param_description }}
     {% endfor -%}
     *
     * @return {{ method_data['return_type'] }} - {{ method_data['return_desc'] }}
     */
    public function {{ method_name }}({% for param_name, param_type, _ in method_data['params'] %}{{ param_type }} ${{ param_name }}{% if not loop.last %}, {% endif %}{% endfor %})
    {
        {{ method_data['body'] }}
    }
    {% endfor %}
}
"""
template_repository_interface = r"""
<?php

namespace App\Repositories;

/**
 * Interface {{ entity_name }}RepositoryInterface
 * @package App\Repositories
 */
interface {{ entity_name }}RepositoryInterface
{
    {% for method_name, method_data in methods.items() %}
    /**
     * {{ method_data['description'] }}
     *
     {% for param_name, param_type, param_description in method_data['params'] -%}
     * @param {{ param_type }} ${{ param_name }} - {{ param_description }}
     {% endfor -%}
     * @return {{ method_data['return_type'] }} - {{ method_data['return_desc'] }}
     */
    public function {{ method_name }}({% for param_name, param_type, _ in method_data['params'] %}{{ param_type }} ${{ param_name }}{% if not loop.last %}, {% endif %}{% endfor %});
    {% endfor %}
}
"""

template_repository = r"""
<?php

namespace App\Repositories;

use App\Models\{{ entity_name }}Model;

/**
 * Clase Db{{ entity_name }}Repository
 *
 * Implements the {{ entity_name }}RepositoryInterface interface using a {{ entity_name | lower}} model.
 *
 * @package App\Repositories
 */
class Db{{ entity_name }}Repository implements {{ entity_name }}RepositoryInterface
{
    /**
     * @var {{ entity_name }}Model The {{ entity_name | lower }} model used by the repository.
     */
    protected ${{ entity_name | lower }}Model;

    /**
     * Db{{ entity_name }}Repository Constructor.
     *
     * @param {{ entity_name }}Model ${{ entity_name | lower }}Model The {{ entity_name | lower }} model to be used.
     */
    public function __construct({{ entity_name }}Model ${{ entity_name | lower }}Model)
    {
        $this->{{ entity_name | lower }}Model = ${{ entity_name | lower }}Model;
    }
    {% for method_name, method_data in methods.items() %}
    /**
     * {{ method_data['description'] }}
     *
     {% for param_name, param_type, param_description in method_data['params'] -%}
     * @param {{ param_type }} ${{ param_name }} - {{ param_description }}
     {% endfor -%}
     *
     * @return {{ method_data['return_type'] }} - {{ method_data['return_desc'] }}
     */
    public function {{ method_name }}({% for param_name, param_type, _ in method_data['params'] %}{{ param_type }} ${{ param_name }}{% if not loop.last %}, {% endif %}{% endfor %})
    {
    
    }
    {% endfor %}
}
"""

template_routes = r"""
<?php

use Slim\Routing\RouteCollectorProxy;
use App\Controllers\{{ entity_name }}Controller;

/**
 * File of routes related to {{ entities_name | lower }}.
 *
 * This file defines the routes for managing {{ entities_name | lower }} in the application.
 *
 * @param \Slim\App $app Instance of the Slim application.
 */

return function ($app) {
    $app->group('/api/{{ entities_name | lower }}', function (RouteCollectorProxy $group) {
        {% for method_name, method_data in methods.items() %}
        /**
         * {{ method_data['description'] }}
         *
         * @method {{ method_data['req_method'] }}
         * @endpoint /api/{{ entities_name | lower }}{{ method_data['endpoint'] }}
         */
        $group->{{ method_data['req_method'] | lower }}('{{ method_data['endpoint'] }}', {{ entity_name }}Controller::class . ':{{ method_data["controller_method"] }}');
        {% endfor %}
    });
};
"""

def generate_code(template_data):
    template = Template(template_data["template"])
    return template.render(common_values, methods=template_data["methods"])

if __name__ == "__main__" :
    parser = ArgumentParser(
    description='''
The script generates a basic directory and code file structure to kickstart the
development of a Slim API, adhering to the Repositories design architecture in
conjunction with MVC design principles.''', formatter_class=RawTextHelpFormatter)
    parser.add_argument('entities', metavar='entities', type=str, nargs='+',
        help='Uno o más nombres de entidades en inglés separados por espacio')
    args = parser.parse_args()
    entities_list = args.entities
    for entity in entities_list:
        entity_name_variations = EntityNameVariations(entity);     
        
        common_values = {
            "entity_name" : f"{entity_name_variations.capitalized}",
            "entities_name" : f"{entity_name_variations.capitalized_pl}",
        }

        templates_data = [
            {"template": template_model, 
             "methods": get_model_methods(entity_name_variations),
             "file": f"./app/Models/{entity_name_variations.capitalized}Model.php"},
            {"template": template_controller, 
             "methods": get_controller_methods(entity_name_variations),
             "file": f"./app/Controllers/{entity_name_variations.capitalized}Controller.php"},
            {"template": template_repository, 
             "methods": get_repository_methods(entity_name_variations),
             "file": f"./app/Repositories/{entity_name_variations.capitalized}RepositoryInterface.php"},
            {"template": template_repository_interface, 
             "methods": get_repository_interface_methods(entity_name_variations),
             "file": f"./app/Repositories/Db{entity_name_variations.capitalized}Repository.php"},
            {"template": template_routes, 
             "methods": get_routes_methods(entity_name_variations),
             "file": f"./app/Routes/{entity_name_variations.lowercase}Routes.php"}
        ]
        
        for template_data in templates_data:
            output_code = generate_code(template_data)
            output_file_path = template_data["file"]
            os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
            with open(output_file_path, 'w') as output_file:
                output_file.write(output_code)
                
            print(f"Código generado para {output_file_path}")

        print("Todos los archivos generados")        