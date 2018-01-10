import numpy as np
import random

class point:
   def __init__(self,x0,y0,z0):
      self.x = x0
      self.y = y0
      self.z = z0

   def __str__(self):
      return "Point(%s,%s,%s)"%(self.x, self.y, self.z)

class tetrahedron:
   def __init__(self,p0,p1,p2,p3):
      self.p0 = p0
      self.p1 = p1
      self.p2 = p2
      self.p3 = p3

   def __str__(self):
      return "Tetrahedron(%s,%s,%s,%s)"%(self.p0
                                       , self.p1
                                       , self.p2
                                       , self.p3)

def random_point_on_sphere(center, radius):
   '''points are generated on the sphere using equtions
      x = x0 + R * cos(theta) * cos(phi)
      y = y0 + R * cos(theta) * sin(phi)
      z = z0 + R * sin(theta)
      where [x0,y0,z0] is a sphere center, phi(0,2*PI), theta(-PI/2, PI/2)'''
   pseudo_randomic_very_important = random.random()
   theta = (pseudo_randomic_very_important * np.pi) - (np.pi/2)

   pseudo_randomic_very_important = random.random()
   phi = pseudo_randomic_very_important * np.pi * 2


   tmp = point(center.x + radius*np.cos(theta)*np.cos(phi)
              ,center.y + radius*np.cos(theta)*np.sin(phi)
              ,center.z + radius*np.sin(phi))
   return tmp

# sphere params hardcode
sphere_center = point(0,0,0)
sphere_radius = 10

# monte carlo
observ = 0
positiv_observ = 0

#generate 4 points which create tetrahedron
for j in range(0,100000):
   tetra = tetrahedron(random_point_on_sphere(sphere_center,sphere_radius)
                      ,random_point_on_sphere(sphere_center,sphere_radius)
                      ,random_point_on_sphere(sphere_center,sphere_radius)
                      ,random_point_on_sphere(sphere_center,sphere_radius))

   #calculating 5 determinants to check if spehre center is inside tetrahedron
   #http://steve.hollasch.net/cgindex/geometry/ptintet.html
   matrix_to_det0 = [[tetra.p0.x , tetra.p0.y , tetra.p0.z , 1]
                    ,[tetra.p1.x , tetra.p1.y , tetra.p1.z , 1]
                    ,[tetra.p2.x , tetra.p2.y , tetra.p2.z , 1]
                    ,[tetra.p3.x , tetra.p3.y , tetra.p3.z , 1]]

   matrix_to_det1 = [[sphere_center.x , sphere_center.y , sphere_center.z , 1]
                    ,[tetra.p1.x , tetra.p1.y , tetra.p1.z , 1]
                    ,[tetra.p2.x , tetra.p2.y , tetra.p2.z , 1]
                    ,[tetra.p3.x , tetra.p3.y , tetra.p3.z , 1]]

   matrix_to_det2 = [[tetra.p0.x , tetra.p0.y , tetra.p0.z , 1]
                    ,[sphere_center.x , sphere_center.y , sphere_center.z , 1]
                    ,[tetra.p2.x , tetra.p2.y , tetra.p2.z , 1]
                    ,[tetra.p3.x , tetra.p3.y , tetra.p3.z , 1]]

   matrix_to_det3 = [[tetra.p0.x , tetra.p0.y , tetra.p0.z , 1]
                    ,[tetra.p1.x , tetra.p1.y , tetra.p1.z , 1]
                    ,[sphere_center.x , sphere_center.y , sphere_center.z , 1]
                    ,[tetra.p3.x , tetra.p3.y , tetra.p3.z , 1]]

   matrix_to_det4 = [[tetra.p0.x , tetra.p0.y , tetra.p0.z , 1]
                    ,[tetra.p1.x , tetra.p1.y , tetra.p1.z , 1]
                    ,[tetra.p2.x , tetra.p2.y , tetra.p2.z , 1]
                    ,[sphere_center.x , sphere_center.y , sphere_center.z , 1]]

   D0 = np.linalg.det(matrix_to_det0)
   D1 = np.linalg.det(matrix_to_det1)
   D2 = np.linalg.det(matrix_to_det2)
   D3 = np.linalg.det(matrix_to_det3)
   D4 = np.linalg.det(matrix_to_det4)

#point is inside tetrahedron if all dets have the same sign
   if D0 != 0:
       if (D0>=0 and D1>=0 and D2>=0 and D3>=0 and D4>=0) or (D0<0 and D1<0 and D2<0 and D3<0 and D4<0):
           positiv_observ+=1
       observ+=1
   if observ%10000 == 0 and observ>1:
       print(observ, positiv_observ)

print('end', observ, positiv_observ)
