import music

def add_music():
    path_file = "music/"
    osu_file: str = input("Digite o arquivo osu da musica.\n")
    music_file: str = input("Digite o arquivo da musica.\n")
    music.readchart_files(path_file + osu_file, path_file + music_file)

def user_input() -> str:
    selected_music: str = input("Digite o nome da musica.\n")

    return selected_music


#add_music()