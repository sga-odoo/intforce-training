from odoo import http
from odoo.http import request


class website_test(http.Controller):

    @http.route("/test_page/", auth="user")
    def test_one(self, **kw):
        #import pdb;pdb.set_trace()
        return "<h1>Hello World</h1>"

    @http.route('/hello/world_1', auth='public')
    def test_controller_1(self):
        return "Hello World"

    @http.route('/hello/world_2', auth='public')
    def test_controller_2(self):
        return "<b>Hello World</b>"

    @http.route('/hello/world_3', auth='public')
    def test_controller_3(self):
        course = request.env['openacademy.course'].search([])
        html = """
        <html>
            <head></head>
            <body>
                <table border='1'>
                    <tr>
                        <th>
                            Course ID
                        </th>
                        <th>
                            Course Name
                        </th>
                    </tr>
                    <tr>
                        <td>
                            %s
                        </td>
                        <td>
                        %s
                        </td>
                    </tr>
                </table>
            </body>
        </html>
        """
        return html % (course.id, course.name)

    @http.route('/static_page', auth='public', website=True)
    def static_controller(self):
        return request.render("intforce.static_page", {})

    @http.route('/dynamic_page', auth='user', website=True)
    def dynamic_controller(self, **kw):
        return request.render("intforce.dynamic_page", {
            "user": request.env.user,
            "test_def": self.test_abc,
            "display": True,
            "arr": [1, 2, 3, 4, 5, 6]
        })

    def test_abc(self):
        return "Test string from function"

    @http.route("/intforce/courses", auth="public", website=True)
    def openacademy_courses(self, **kw):
        courses = request.env['openacademy.course'].search([])
        return request.render("intforce.courses", {
            'courses': courses
        })

    @http.route("/intforce/courses/<model('openacademy.course'):course>", auth="public", website=True)
    def openacademy_course_detail(self, course, **kw):
        return request.render("intforce.courses_detail", {
            'course': course
        })
