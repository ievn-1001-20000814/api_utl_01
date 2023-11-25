from flask import Flask, request
from flask_mysqldb import MySQL
from config import config

app=Flask(__name__)


con=MySQL(app)

@app.route('/alumnos',methods=['GET'])
def lista_alumnos():
    try :
        cursor=con.connection.cursor()
        sql='select * from alumnos'
        cursor.execute(sql)
        datos=cursor.fechall()
        alumnos=[]
        for fila in datos:
            alumno={'matricula':fila[0],'nombre':fila[1],'apaterno':fila[2]
                     ,'amaterno':fila[3], 'correo': fila[4]}
            alumnos.append(alumno)
            print(alumnos)
        return jsonify({'alumnos':alumnos,'mensaje':'Lista de Alumnos','exito':True})
    
    except Exception as ex:
        return jsonify({'mensaje':'error {}'.format(ex),'exito':False})


def leer_alumno_bd(matricula):
    try :
        cursor=con.connection.cursor()
        sql='select * from alumnos where matricula= {0}'.formar(matricula)
        cursor.execute(sql)
        datos=cursor.fechone()

        if datos != None:
            alumno={'matricula':datos[0],'nombre':datos[1],'apaterno':datos[2],'amaterno':datos[3], 'correo': datos[4]}
            return alumno
        else:
            return None

    except Exception as ex:
        return ex

@app.route('/alumnos/<mat>', methods=['GET'])
def leer_alumno(mat):
    try :
        alumno=leer_alumno_bd(mat)

        if alumno != None:
            return jsonify({'alumno':alumno,'mensaje':'Alumnos encontrado','exito':True})
        else:
            return jsonify({'alumno':alumno,'mensaje':'Alumno no encontrado','exito':True})
            
        
    
    except Exception as ex:
        return jsonify({'mensaje':'error {}'.format(ex),'exito':False})
    
    
@app.route('/alumnos', methods=['POST'])
def method_name():
    try :
        alumno = leer_alumno_bd(request.json['matricula'])
        if alumno !=None:
            return jsonify({'mensaje':'Alumno ya existe','exito':False})
        else: 
            cursor=con.connection.cursor()
            sql= """ INSERT INTO alumnos(matricula,nombre,apaterno,amaterno,correo)
            VALUES({0},'{1}','{2}','{3}','{4}')""".format(request.json['matricula'],
            request.json['nombre'],request.json['apaterno'],request.json['amaterno'],
            request.json['correo'])
            cursor.execute(sql)
            con.connection.commit()
            return jsonify({'mensaje':'Alumnos registrado','exito':True})
    
    
    except Exception as ex:
        return jsonify({'mensaje':'error {}'.format(ex),'exito':False})





def pagina_no_encontrada(error):
    return "<h1>Pagina no encontrada</h1>",400
if __name__ == "__main__":
    app.config.from_object(config['development'])
    app.register_error_handler(404,pagina_no_encontrada)
    app.run()