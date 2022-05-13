import discord
import sys

from settings import defaultEmbedColor

# returns an embed message obje ct which can then be sent await msg.channel.send(embed=<embedMuuttuja>)
def createEmbed(title=None, desc=None, color=defaultEmbedColor, thumbnail=None, image=None, fields=None):
    embed = discord.Embed(title=title, color=color)
    if desc:
        embed.description = desc

    if thumbnail:
        embed.set_thumbnail(url=thumbnail)

    if image:
        embed.set_image(url=image)

    if type(fields) is list:
        for field in fields:
            if not 'inline' in field.keys():
                field['inline'] = False

            embed.add_field(name=field["name"], value=field["value"], inline=field["inline"])
    elif fields:
        raise(Exception("An Error occured when creating an embed message - {}.\nError: Fields-argument has to be a list of dictionaries, even if there's only one.".format(title)))

    return embed

def detailed_exc_msg(e: Exception) -> None:
    """Prints exception type, file, and line number."""
    exception_traceback = sys.exc_info()[2]
    filename = exception_traceback.tb_frame.f_code.co_filename
    line_number = exception_traceback.tb_lineno

    print(f"{e=}, {type(e)=}")
    print("File name: ", filename)
    print("Line number: ", line_number)
