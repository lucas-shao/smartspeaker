import vlc
import time
import threading


class MusicPlayer:
    def __init__(self, url):
        self.player = vlc.MediaPlayer(url)

    def play(self):
        if self.player.get_state() in [
            vlc.State.NothingSpecial,
            vlc.State.Paused,
            vlc.State.Stopped,
        ]:
            self.player.play()
        else:
            print("Already playing music")

    def pause(self):
        if self.player.get_state() == vlc.State.Playing:
            self.player.pause()
        else:
            print("Music is not currently playing")

    def stop(self):
        self.player.stop()


def player_thread(player):
    # 播放音乐
    player.play()
    # 等待5秒
    time.sleep(10)
    # 暂停音乐
    player.pause()
    # 等待5秒
    time.sleep(3)
    # 继续播放音乐
    player.play()
    # 等待60秒
    time.sleep(60)


def main():
    player = MusicPlayer(
        "/Users/shaoshuai.shao/iWorks/source/Musicer/download/一起走过的日子-刘德华.mp3"
    )
    thread = threading.Thread(target=player_thread, args=(player,))
    thread.start()
    thread.join()


if __name__ == "__main__":
    main()
