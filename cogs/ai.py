import os
import discord
from discord import app_commands
from discord.ext import commands
from openai import OpenAI

class LewisAI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    @app_commands.command(name="ask", description="Ask LEWIS AI.")
    @app_commands.describe(prompt="Your question for Lewis?")
    async def ask_slash(self, interaction, prompt: str): 
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You're Lewis, a nonchalant, dry humored AI. Your answering every question as if it's obvious. Its supposed to be nonchalant, and not corny. Your task is to help users with their questions."},
                    {"role": "user", "content": prompt},
                ],
            )

            answer = response.choices[0].message.content.strip()
            
            embed = discord.Embed(
                title="Lewis AI",
                description=answer,
                color=discord.Color.blue()
            )
            embed.set_footer(text=f"Asked by {interaction.user.display_name}")
            
            await interaction.followup.send(embed=embed)

        except Exception as e:
            await interaction.followup.send(f"Error: {e}")

async def setup(bot):
    await bot.add_cog(LewisAI(bot))