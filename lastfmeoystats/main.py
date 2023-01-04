""" Create lists and graphs for end of the year last.fm stats."""

from datetime import datetime
import json
import matplotlib.pyplot as plt  # type: ignore
import pylast


def get_secrets():
    try:
        with open('secrets.json', 'r') as file:
            secrets = json.load(file)
            return secrets
    except FileNotFoundError:
        print("Could not find secrets.json!")
        raise


def interpret_secrets(secrets: dict):
    """Use data from secrets.json to get user data from last.fm.

    :param secrets: A dictionary with API and user data.
    :returns: A pylast user object.
    """
    api_key = secrets['key']
    api_secret = secrets['secret']
    user = secrets['user']
    network = pylast.LastFMNetwork(api_key=api_key, api_secret=api_secret)
    user = network.get_user(user)
    return user


def get_annual_data(user):
    """Get annual data from last.fm.

    :param user: A pylast user object
    :returns: A tuple with the top artists, albums, and tracks of the last 12 months.
    """
    return user.get_top_artists(period='12month', limit=20), user.get_top_albums(period='12month', limit=20),\
           user.get_top_tracks(period='12month', limit=20)


def get_all_time_data(user):
    """Get overall data from last.fm.

        :param user: A pylast user object
        :returns: A tuple with the top artists, albums, and tracks for the entire user history.
        """
    return user.get_top_artists(period='overall', limit=100), user.get_top_albums(period='overall', limit=15), \
           user.get_top_tracks(period='overall', limit=15)


def write_data_to_file(data, file_name: str):
    """Write data to files in a nice way to copy and past into a blog post.

    :param data: The data from last.fm - an iterable
    :param file_name: The filename to save the data to.
    """
    output = [f'{number + 1}. {lastfm_thing.item} ({lastfm_thing.weight})\n' for number, lastfm_thing in
              enumerate(data)]
    with open(file_name, 'w') as file:
        file.writelines(output)


def create_bar_chart(last_fm_data, x_label: str = "", y_label: str = "", title: str = "",
                     graph_path: str = "", graph_filename: str = ""):
    """Create matplotlib bar graph.

    :param last_fm_data: last.fm iterable data
    :param x_label: The label for the x-axis on the graph.
    :param y_label: The label for the y-axis on the graph.
    :param title: The Title for the graph.
    :param graph_path: The path to save the graph to.
    :param graph_filename: The filename to give the png file of the graph.
    """
    plt.style.use('fivethirtyeight')
    plt.rcParams.update({'figure.autolayout': True})
    fig, ax = plt.subplots(figsize=(25, 25))
    names = [f'{last_fm_thing.item}' for last_fm_thing in last_fm_data]
    listens = [int(last_fm_thing.weight) for last_fm_thing in last_fm_data]
    ax.bar(names, listens)
    x_labels = ax.get_xticklabels()
    plt.setp(x_labels, rotation=50, horizontalalignment='right')
    ax.set(xlabel=x_label, ylabel=y_label, title=title)
    ax.title.set(y=1.05)
    fig.savefig(f"{graph_path}/{graph_filename}", transparent=False, dpi=80, bbox_inches="tight")


if __name__ == '__main__':
    my_secrets = get_secrets()
    my_user = interpret_secrets(my_secrets)
    top_annual_artists, top_annual_albums, top_annual_tracks = get_annual_data(my_user)
    top_overall_artists, top_overall_albums, top_overall_tracks = get_all_time_data(my_user)
    current_year = datetime.now().year
    write_data_to_file(top_annual_artists, "top_annual_artists")
    create_bar_chart(top_annual_artists, 'Artists', 'Listens', f'Top Artists of {current_year}', '.',
                     'top_annual_artist.jpg')
    write_data_to_file(top_overall_artists, "top_overall_artists")
    create_bar_chart(top_overall_artists, 'Artists', 'Listens', 'Top Artists Overall', '.',
                     'top_overall_artist.jpg')
    write_data_to_file(top_annual_albums, "top_annual_albums")
    create_bar_chart(top_annual_albums, 'Albums', 'Listens', f'Top Albums of {current_year}', '.',
                     'top_annual_albums.jpg')
    write_data_to_file(top_overall_albums, "top_overall_albums")
    create_bar_chart(top_overall_albums, 'Albums', 'Listens', 'Top Albums Overall', '.', 'top_overall_albums.jpg')
    write_data_to_file(top_annual_tracks, "top_annual_tracks")
    create_bar_chart(top_annual_tracks, 'Tracks', 'Listens', f'Top Tracks of {current_year}', '.',
                     'top_annual_tracks.jpg')
    write_data_to_file(top_overall_tracks, "top_overall_tracks")
    create_bar_chart(top_overall_tracks, 'Tracks', 'Listens', 'Top Tracks Overall', '.', 'top_overall_tracks.jpg')
