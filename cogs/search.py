import discord
from discord.ext import commands
from youtubesearchpython import SearchVideos
import requests
import datetime
from googleapiclient.discovery import build
import asyncio


my_api_key = "AIzaSyCfhRAX4kFCgYK74V0jS5gcQGuSme3xnew"
my_cse_id = "219201fb9a78217af"

im_api_key = 'AIzaSyCAzp0H-a3xlEwSFmxx1QzL_ZwWK3_1yxU'
im_cse_id = '71c58d7741f6fddbc'


def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res
  
  
def image_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res


class Search(commands.Cog):
    """Search Category"""

    def __init__(self, client):
        self.client = client

    
    @commands.command(
        aliases=['yt', 'video', 'videos'],
        usage='<youtube [term]',
        brief='Searches YouTube for provided term'
    )
    async def youtube(self, ctx, *, query=None):

        if not query:
            return await ctx.send("You didn't tell me what to search for")

        search = SearchVideos(f"{query}", offset=1, mode="dict", max_results=1)

        search = search.result()

        await ctx.reply(search['search_result'][0]['link'], mention_author=False)

    
    @commands.command(
        aliases=['search'],
        usage='<google [term]',
        brief='Searches Google for provided term'
    )
    async def google(self, ctx, *, query=None):

        if not query:
            return await ctx.send("You didn't tell me what to search for")

        try:
            result = google_search(query, my_api_key, my_cse_id)

            res = result['items'][0]

            e = discord.Embed(
                title=f"{res['title']}",
                url=f"{res['link']}",
                description=f"{res['snippet']}"
            )

            e.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar_url)

            await ctx.reply(embed=e, mention_author=False)

        except:
            em = discord.Embed(description=f"I couldn't find any matched on Google")
            await ctx.reply(embed=em, mention_author=False)


    @commands.command(
        aliases=['ub', 'urbandictionary'],
        usage='<urban [term]',
        brief='Searches Urban Dictionary for provided term'
    )
    async def urban(self, ctx, *, word=None):
        try:
            word_a = str(word)

            word_r = word_a.replace(" ", "+")

            url = 'http://api.urbandictionary.com/v0/define?term=' + word_r

            x = requests.get(url)

            resp = x.json()

            defin = resp['list'][0]['definition']
            ex = resp['list'][0]['example']

            a = defin.translate({ord('['): None})
            final_def = a.translate({ord(']'): None})

            b = ex.translate({ord('['): None})
            final_ex = b.translate({ord(']'): None})

            em = discord.Embed(description=f"{final_def}\n\n*{final_ex}*")
            em.set_author(name=f"Urban Dictionary — {resp['list'][0]['word']}", icon_url='https://i.imgur.com/he2iV0Y.png')
            await ctx.reply(embed=em, mention_author=False)

        except:
            em = discord.Embed(
                description=f"No definitions found for '{word}'"
            )

            await ctx.reply(embed=em, mention_author=False)


    @commands.command(
        usage='<movie [term]',
        brief='Searched for a movie by provided name'
    )
    async def movie(self, ctx, *, arg=None):

        if not arg:
            return await ctx.reply("You didn't tell me what movie to search for", mention_author=False)

        url = "http://www.omdbapi.com/?apikey=e3d6a084&"
        year = ''
        params = {
            't' : arg,
            'type' : 'movie',
            'y' : year,
            'plot' : 'full'
        }
        response = requests.get(url, params=params).json()
        try:
            title = response['Title']
            year = response['Year']
            rated = response['Rated']
            released = response['Released']
            runtime = response['Runtime']
            genre = response['Genre']
            director = response['Director']
            actors = response['Actors']
            plot = response['Plot']
            language = response['Language']
            poster = response['Poster']
            imdb_ratings = response['imdbRating']
            production = response['Production']

            embed = discord.Embed(
                title=f'Movie Search — {title}',
            )    

            embed.set_thumbnail(url = poster)

            embed.add_field(name=':page_with_curl: Title', value = title, inline = False)
            embed.add_field(name=':grey_question: Rated', value = rated, inline = False)
            embed.add_field(name=':calendar_spiral: Year', value = year, inline = False)
            embed.add_field(name=':calendar: Released', value = released, inline = False)
            embed.add_field(name=':triangular_flag_on_post: Genre', value = genre, inline = False)
            embed.add_field(name=':clock1030: Runtime', value = runtime, inline = False)
            embed.add_field(name=':mega: Director', value = director, inline = False)
            embed.add_field(name=':person_curly_hair: Actors', value = actors, inline = False)
            embed.add_field(name=':page_with_curl: Synopsis', value = plot, inline = False)
            embed.add_field(name=':speech_left: Languages', value = language, inline = False)
            embed.add_field(name=':star: IMdB ratings', value = imdb_ratings, inline = False)
            embed.add_field(name=':mega: Production', value = production, inline = False)
            await ctx.reply(embed=embed, mention_author=False)
        
        except:
            await ctx.reply(f"I couldn't find any movied by that name in the database", mention_author=False)


    @commands.command(
        aliases=['lyric', 'ly'],
        usage='<lyrics [song]',
        brief="Returns lyrics for song"
    )
    async def lyrics(self, ctx, *, title: str = None):
        if not title:
            await ctx.reply("You didn't tell me what song to fetch the lyrics for\nUsage: `<lyrics [song name]` (Specify author name for more precise results)", mention_author=False)
            return

        title.replace(" ", "+")

        url = "https://some-random-api.ml/lyrics?title=" + title

        r = requests.request('GET', url).json()

        try:
            if r['error']:
                await ctx.send("I couldn't find lyrics for that song")
                return
            else:
                pass

        except:
            pass

        description = r['lyrics']

        if len(description) > 2000:
            description = description[:2000] + "..."

        em = discord.Embed(
            title=f"{r['title']} - {r['author']}", url=f"{r['links']['genius']}",
            description=description

        )

        em.set_thumbnail(url=f"{r['thumbnail']['genius']}")

        em.set_footer(text="Didn't get what you're looking for? Try adding the author's name to the search")

        await ctx.reply(embed=em, mention_author=False)
        
        
    @commands.command(
        usage='<game [name]',
        brief='Returns info for game'
    )
    async def game(self, ctx, *, search=None):

        if not search:
            await ctx.reply(embed=discord.Embed(description="You didn't give me a game to search for"), mention_author=False)

        search = search.strip(" ")

        search = search.replace(" ", "-")

        url = f"https://api.rawg.io/api/games/{search}?key=3984a58125dc4ddd890f5397fd9ccb09"

        response = requests.request("GET", url).json()

        try:
            name = response['name']
            released = response['released']
            image = response['background_image']
            website = response['website']
            rating = response['rating']
            description = str(response['description_raw']).replace("###", "#")
            if len(description) > 1500:
                description = description[:1500] + "..."

            platforms_raw = response['parent_platforms']

            platforms = []

            for i in platforms_raw:
                platforms.append(i['platform']['name'])

            em = discord.Embed(title=f"{name}", url=f"{website}", description=f"{description}")

            em.set_thumbnail(url=f"{image}")

            em.add_field(name="Released", value=f"{released}", inline=False)
            em.add_field(name="Rating", value=f"{rating}", inline=False)
            em.add_field(name="Website", value=f"{website}", inline=False)
            em.add_field(name="Platforms", value=", ".join(platforms), inline=False)

            await ctx.reply(embed=em, mention_author=False)

        except:
            await ctx.reply(embed=discord.Embed(description="No results found for term, be specific with the name"), mention_author=False)

   
def setup(client):
    client.add_cog(Search(client))
