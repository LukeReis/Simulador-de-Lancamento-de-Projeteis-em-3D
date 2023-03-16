from vpython import *

angulo1 = float(input("Insira o angulo de lançamento da bola AMARELA: "))
angulo2 = float(input("Insira o angulo de lançamento da bola VERMELHA: "))
angulo3 = float(input("Insira o angulo de lançamento da bola LARANJA: "))

altura_maxima = {"AMARELA": 0, "VERMELHA": 0, "LARANJA": 0}



def deslocar(corpo):
    global dt
    queda = True
    p = corpo.traj.point(corpo.traj.npoints - 1)['pos']
    corpo.pos += dt * corpo.v + dt ** 2 * corpo.a / 2.
    if corpo.v.y < 0 and corpo.pos.y < corpo.radius:
        if p.y != corpo.pos.y:
            f = (p.y - corpo.radius) / (p.y - corpo.pos.y)
            corpo.pos -= (1 - f) * (corpo.pos - p)
            corpo.v += f * dt * corpo.a
            corpo.t += f * dt
        queda = False
    else:
        corpo.t += dt
        corpo.v += dt * corpo.a

    if not queda and p.y > corpo.pos.y:
        altura_maxima[corpo.legenda] = p.y - corpo.radius

    corpo.traj.append(pos=vec(corpo.pos))
    corpo.d += mag(corpo.pos - p)

    return queda


def resultados(corpo):
    p0 = corpo.traj.point(0)['pos']
    alcance = corpo.pos.x - p0.x
    velocidade = corpo.d / corpo.t
    scene.caption += '<b>' + corpo.legenda + '</b>\n'
    scene.caption += 'Tempo no ar         = {:.2f} s\n'.format(corpo.t)
    scene.caption += 'Distancia horizontal   = {:.2f} m\n'.format(alcance)
    scene.caption += 'Distância percorrida = {:.2f} m\n'.format(corpo.d)
    scene.caption += 'Velocidade média     = {:.2f} m/s\n'.format(velocidade)
    scene.caption += 'Altura máxima alcançada = {:.2f} m\n'.format(altura_maxima[corpo.legenda])

    return


def projetar(corpo, vel, ang, leg):
    vel = float(input(f"Insira a velocidade de arremesso para {leg} (m/s): "))
    corpo.v = vel * vec(cos(ang * pi / 180.), sin(ang * pi / 180.), 0)
    corpo.t = corpo.d = 0
    corpo.legenda = leg
    corpo.traj = curve(pos=vec(corpo.pos), color=corpo.color)


def exibir_altura_maxima():
    scene.append_to_caption('\n')
    for leg, altura in altura_maxima.items():
        scene.append_to_caption(f"Altura máxima da {leg}: {altura:.2f} m\n")


scene = canvas(title='<h1>ANALISE DE FENOMENOS FISICOS DA NATUREZA</h1>',
               forward=vec(-0.5, -0.2, -1))
scene.caption = ''
a = 47.
dt = 0.01
g = vec(0, -9.8, 0)
q1 = q2 = q3 = True

bola1 = sphere(pos=vec(-7.5, 0.2, 1), radius=0.4, color=vec(0.93, 1, 0.16))
bola2 = sphere(pos=vec(-7.5, 0.1, 0), radius=0.4, color=vec(1, 0, 0))
bola3 = sphere(pos=vec(-7.5, 0.1, -1), radius=0.4, color=vec(1, 0.49, 0.05))
chao = box(pos=vec(0, -0.1, 0), size=vec(16, 0.2, 10), texture=textures.wood)
parede = box(pos=vec(0, 2.8, -5.05), size=vec(16, 6, 0.1), color=vec(0.7, 0.7, 0.7))
sitio = text(pos=vec(0, 2.8, -5), text='AFFN', color=color.blue,
             align='center', depth=0)

projetar(bola1, 10, angulo1, 'Bola de ténis (AMARELA)')
projetar(bola2, 10, angulo2, 'Sem resistência do ar (VERMELHA)')
projetar(bola3, 10, angulo3, 'Bola de ping-pong (LARANJA)')
bola2.a = g

while q1 or q2 or q3:
    rate(100)
    bola1.a = g - 0.01606 * mag(bola1.v) * bola1.v
    bola3.a = g - 0.14176 * mag(bola3.v) * bola3.v
    if q1: q1 = deslocar(bola1)
    if q2: q2 = deslocar(bola2)
    if q3: q3 = deslocar(bola3)

resultados(bola2)
resultados(bola1)
resultados(bola3)
exibir_altura_maxima(bola2)*100
exibir_altura_maxima(bola1)*100
exibir_altura_maxima(bola3)*100
