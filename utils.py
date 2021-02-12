from settings import defaultEmbedColor
import discord

# returns an embed message obje ct which can then be sent await msg.channel.send(embed=<embedMuuttuja>)
def createEmbed(title=None, desc=None, color=defaultEmbedColor, thumbnail=None, image=None, fields=None):
    embed = discord.Embed(title=title, description=desc, color=color)
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
