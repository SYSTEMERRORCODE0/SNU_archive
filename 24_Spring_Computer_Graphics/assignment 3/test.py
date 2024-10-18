import pyglet

# 이미지 파일 로드
image = pyglet.image.load('Free_rock_tex\Free_rock_Normal_OpenGL.jpg')

# 새 창 생성
window = pyglet.window.Window()

@window.event
def on_draw():
    window.clear()
    sprite = pyglet.sprite.Sprite(image)
    sprite.draw()

# 애플리케이션 실행
pyglet.app.run()