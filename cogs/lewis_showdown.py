import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import Button, View
import random
import json
import os
from typing import Optional

# character details
CHARACTERS = {
    "Mekhi": {
        "class": "Tank",
        "hp": 150,
        "attack": 15,
        "defense": 10,
        "special": "Bull Shield",
        "special_desc": "Reduces damage taken by 50% for 2 turns",
        "emoji": "💪🏿",
        "image_url": "https://media.discordapp.net/attachments/1183640136978792448/1452487948460232845/FA5E0F40-AFA1-49CD-8ECD-5044F35C1F7E.jpg?ex=6949fe50&is=6948acd0&hm=5c71a31c40776bcc1d8f062ccc225c469a30ebc98fa5213da268acb3fc5dc2e9&=&format=webp&width=615&height=885",
    },
    "Elly": {
        "class": "Tank",
        "hp": 150,
        "attack": 15,
        "defense": 10,
        "special": "Lunar Light",
        "special_desc": "Reduces damage taken by 50% for 2 turns",
        "emoji": "🌌",
        "image_url": "https://media.discordapp.net/attachments/1183640136978792448/1452487948460232845/FA5E0F40-AFA1-49CD-8ECD-5044F35C1F7E.jpg?ex=6949fe50&is=6948acd0&hm=5c71a31c40776bcc1d8f062ccc225c469a30ebc98fa5213da268acb3fc5dc2e9&=&format=webp&width=615&height=885",
    },
    "Lewis": {
        "class": "Damage",
        "hp": 100,
        "attack": 30,
        "defense": 5,
        "special": "Card Strike",
        "special_desc": "Deals 2x damage",
        "emoji": "🪪",
        "image_url": "https://media.discordapp.net/attachments/1183640136978792448/1452487948460232845/FA5E0F40-AFA1-49CD-8ECD-5044F35C1F7E.jpg?ex=6949fe50&is=6948acd0&hm=5c71a31c40776bcc1d8f062ccc225c469a30ebc98fa5213da268acb3fc5dc2e9&=&format=webp&width=615&height=885"
    },
    "Drago": {
        "class": "Damage",
        "hp": 150,
        "attack": 15,
        "defense": 10,
        "special": "Parry",
        "special_desc": "Parry an upcoming attack, hitting the enemy with half its damage.",
        "emoji": "🐦‍⬛",
        "image_url": "https://media.discordapp.net/attachments/1183640136978792448/1452487948460232845/FA5E0F40-AFA1-49CD-8ECD-5044F35C1F7E.jpg?ex=6949fe50&is=6948acd0&hm=5c71a31c40776bcc1d8f062ccc225c469a30ebc98fa5213da268acb3fc5dc2e9&=&format=webp&width=615&height=885",
    },
    "Ashton": {
        "class": "Damage",
        "hp": 150,
        "attack": 15,
        "defense": 10,
        "special": "Illusion",
        "special_desc": "",
        "emoji": "🌀",
        "image_url": "https://media.discordapp.net/attachments/1183640136978792448/1452487948460232845/FA5E0F40-AFA1-49CD-8ECD-5044F35C1F7E.jpg?ex=6949fe50&is=6948acd0&hm=5c71a31c40776bcc1d8f062ccc225c469a30ebc98fa5213da268acb3fc5dc2e9&=&format=webp&width=615&height=885",
    },
    "Santi": {
        "class": "Healer",
        "hp": 150,
        "attack": 15,
        "defense": 10,
        "special": "Bull Shield",
        "special_desc": "Reduces damage taken by 50% for 2 turns",
        "emoji": "🎩",
        "image_url": "https://media.discordapp.net/attachments/1183640136978792448/1452487948460232845/FA5E0F40-AFA1-49CD-8ECD-5044F35C1F7E.jpg?ex=6949fe50&is=6948acd0&hm=5c71a31c40776bcc1d8f062ccc225c469a30ebc98fa5213da268acb3fc5dc2e9&=&format=webp&width=615&height=885",
    },
    "Jordan": {
        "class": "Healer",
        "hp": 120,
        "attack": 20,
        "defense": 7,
        "special": "Grimoire Heal",
        "special_desc": "Restores 40 HP",
        "emoji": "🧑‍🎨",
        "image_url": "https://media.discordapp.net/attachments/1183640136978792448/1452487948460232845/FA5E0F40-AFA1-49CD-8ECD-5044F35C1F7E.jpg?ex=6949fe50&is=6948acd0&hm=5c71a31c40776bcc1d8f062ccc225c469a30ebc98fa5213da268acb3fc5dc2e9&=&format=webp&width=615&height=885"
    }
}

# data file for player data
class PlayerData:
    def __init__(self):
        self.data_file = "player_data.json"
        self.data = self.load_data()
    
    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                return json.load(f)
        return {}
    
    def save_data(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.data, f, indent=4)
    
    def get_player(self, user_id):
        user_id = str(user_id)
        if user_id not in self.data:
            self.data[user_id] = {"gold": 100, "wins": 0, "losses": 0}
            self.save_data()
        return self.data[user_id]
    
    def add_gold(self, user_id, amount):
        user_id = str(user_id)
        player = self.get_player(user_id)
        player["gold"] += amount
        self.save_data()
    
    def add_win(self, user_id):
        user_id = str(user_id)
        player = self.get_player(user_id)
        player["wins"] += 1
        self.save_data()
    
    def add_loss(self, user_id):
        user_id = str(user_id)
        player = self.get_player(user_id)
        player["losses"] += 1
        self.save_data()

# battle state for tracking progress
class BattleState:
    def __init__(self, p1_id, p2_id, p1_char, p2_char):
        self.p1_id = p1_id
        self.p2_id = p2_id
        self.p1_char = p1_char
        self.p2_char = p2_char
        
        # Initialize stats
        self.p1_hp = CHARACTERS[p1_char]["hp"]
        self.p1_max_hp = CHARACTERS[p1_char]["hp"]
        self.p2_hp = CHARACTERS[p2_char]["hp"]
        self.p2_max_hp = CHARACTERS[p2_char]["hp"]
        
        self.p1_shield = 0
        self.p2_shield = 0
        self.turn = 1
        self.battle_log = []
        self.winner = None

# battle view for handling interactions
class BattleView(View):
    def __init__(self, battle_state: BattleState, player_data: PlayerData):
        super().__init__(timeout=300)
        self.battle = battle_state
        self.player_data = player_data
    
    def get_current_player(self):
        return self.battle.p1_id if self.battle.turn == 1 else self.battle.p2_id
    
    def create_embed(self):
        p1_char = CHARACTERS[self.battle.p1_char]
        p2_char = CHARACTERS[self.battle.p2_char]
        
        embed = discord.Embed(
            title="LEWIS SHOWDOWN BATTLE",
            color=discord.Color.red() if self.battle.turn == 1 else discord.Color.blue()
        )

        embed.set_thumbnail(url=p1_char["image_url"])
        embed.set_image(url=p2_char["image_url"])
        
        p1_hp_bar = self.create_hp_bar(self.battle.p1_hp, self.battle.p1_max_hp)
        embed.add_field(
            name=f"{p1_char['emoji']} Player 1: {self.battle.p1_char} ({p1_char['class']})",
            value=f"HP: {p1_hp_bar} {self.battle.p1_hp}/{self.battle.p1_max_hp}\n"
                  f"Shield: {'🛡️' * self.battle.p1_shield if self.battle.p1_shield > 0 else 'None'}",
            inline=False
        )
        
        p2_hp_bar = self.create_hp_bar(self.battle.p2_hp, self.battle.p2_max_hp)
        embed.add_field(
            name=f"{p2_char['emoji']} Player 2: {self.battle.p2_char} ({p2_char['class']})",
            value=f"HP: {p2_hp_bar} {self.battle.p2_hp}/{self.battle.p2_max_hp}\n"
                  f"Shield: {'🛡️' * self.battle.p2_shield if self.battle.p2_shield > 0 else 'None'}",
            inline=False
        )
        
        if self.battle.battle_log:
            log_text = "\n".join(self.battle.battle_log[-3:])
            embed.add_field(name="📜 Battle Log", value=log_text, inline=False)
        
        current = "Player 1" if self.battle.turn == 1 else "Player 2"
        embed.set_footer(text=f"Current Turn: {current}")
        
        return embed
    
    def create_hp_bar(self, current, maximum, length=10):
        filled = int((current / maximum) * length)
        bar = "█" * filled + "░" * (length - filled)
        return f"[{bar}]"
    
    async def check_winner(self, interaction):
        if self.battle.p1_hp <= 0:
            self.battle.winner = 2
            return True
        elif self.battle.p2_hp <= 0:
            self.battle.winner = 1
            return True
        return False
    
    async def end_battle(self, interaction):
        for item in self.children:
            item.disabled = True
        
        winner_id = self.battle.p1_id if self.battle.winner == 1 else self.battle.p2_id
        loser_id = self.battle.p2_id if self.battle.winner == 1 else self.battle.p1_id
        winner_char = self.battle.p1_char if self.battle.winner == 1 else self.battle.p2_char
        
        gold_reward = random.randint(50, 150)
        self.player_data.add_gold(winner_id, gold_reward)
        self.player_data.add_win(winner_id)
        self.player_data.add_loss(loser_id)
        
        embed = discord.Embed(
            title="🏆 BATTLE COMPLETE! 🏆",
            description=f"<@{winner_id}> wins with {winner_char}!\n\n"
                       f"💰 Reward: **{gold_reward} Gold**",
            color=discord.Color.gold()
        )
        
        await interaction.response.edit_message(embed=embed, view=self)
    
    @discord.ui.button(label="⚔️ Attack", style=discord.ButtonStyle.danger)
    async def attack_button(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id != self.get_current_player():
            await interaction.response.send_message("It's not your turn.", ephemeral=True)
            return
        
        attacker_is_p1 = self.battle.turn == 1
        
        if attacker_is_p1:
            attacker_char = CHARACTERS[self.battle.p1_char]
            defender_shield = self.battle.p2_shield
        else:
            attacker_char = CHARACTERS[self.battle.p2_char]
            defender_shield = self.battle.p1_shield
        
        damage = attacker_char["attack"]
        
        if defender_shield > 0:
            damage = damage // 2
        
        damage = max(1, damage - (CHARACTERS[self.battle.p2_char if attacker_is_p1 else self.battle.p1_char]["defense"]))
        
        if attacker_is_p1:
            self.battle.p2_hp -= damage
            self.battle.battle_log.append(f"⚔️ Player 1 attacked for {damage} damage!")
        else:
            self.battle.p1_hp -= damage
            self.battle.battle_log.append(f"⚔️ Player 2 attacked for {damage} damage!")
        
        if attacker_is_p1 and self.battle.p1_shield > 0:
            self.battle.p1_shield -= 1
        elif not attacker_is_p1 and self.battle.p2_shield > 0:
            self.battle.p2_shield -= 1
        
        if await self.check_winner(interaction):
            await self.end_battle(interaction)
            return
        
        self.battle.turn = 2 if self.battle.turn == 1 else 1
        await interaction.response.edit_message(embed=self.create_embed(), view=self)
    
    @discord.ui.button(label="✨ Special", style=discord.ButtonStyle.primary)
    async def special_button(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id != self.get_current_player():
            await interaction.response.send_message("It is not your turn yet.", ephemeral=True)
            return
        
        attacker_is_p1 = self.battle.turn == 1
        
        if attacker_is_p1:
            char = CHARACTERS[self.battle.p1_char]
        else:
            char = CHARACTERS[self.battle.p2_char]
        
        if char["class"] == "Tank":
            if attacker_is_p1:
                self.battle.p1_shield = 2
            else:
                self.battle.p2_shield = 2
            self.battle.battle_log.append(f"🛡️ Player {self.battle.turn} used {char['special']}!")
        
        elif char["class"] == "Damage":
            damage = char["attack"] * 2
            defender_def = CHARACTERS[self.battle.p2_char if attacker_is_p1 else self.battle.p1_char]["defense"]
            damage = max(1, damage - defender_def)
            
            if attacker_is_p1:
                self.battle.p2_hp -= damage
            else:
                self.battle.p1_hp -= damage
            self.battle.battle_log.append(f"🔥 Player {self.battle.turn} used {char['special']} for {damage} damage!")
        
        elif char["class"] == "Healer":
            heal = 40
            if attacker_is_p1:
                self.battle.p1_hp = min(self.battle.p1_max_hp, self.battle.p1_hp + heal)
            else:
                self.battle.p2_hp = min(self.battle.p2_max_hp, self.battle.p2_hp + heal)
            self.battle.battle_log.append(f"✨ Player {self.battle.turn} used {char['special']}!")
        
        if attacker_is_p1 and self.battle.p1_shield > 0:
            self.battle.p1_shield -= 1
        elif not attacker_is_p1 and self.battle.p2_shield > 0:
            self.battle.p2_shield -= 1
        
        if await self.check_winner(interaction):
            await self.end_battle(interaction)
            return
        
        self.battle.turn = 2 if self.battle.turn == 1 else 1
        await interaction.response.edit_message(embed=self.create_embed(), view=self)

# main bot class - THIS IS A COG
class LewisShowdown(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.player_data = PlayerData()
        self.pending_battles = {}
    
    @app_commands.command(name="characters", description="View all available characters")
    async def characters(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🎮 Available Characters",
            description="Choose your fighter!",
            color=discord.Color.purple()
        )
        
        for name, data in CHARACTERS.items():
            embed.add_field(
                name=f"{data['emoji']} {name} - {data['class']}",
                value=f"**HP:** {data['hp']}\n"
                      f"**Attack:** {data['attack']}\n"
                      f"**Defense:** {data['defense']}\n"
                      f"**Special:** {data['special']} - {data['special_desc']}",
                inline=False
            )
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="profile", description="View your profile and stats")
    async def profile(self, interaction: discord.Interaction):
        player = self.player_data.get_player(interaction.user.id)
        
        embed = discord.Embed(
            title=f"👤 {interaction.user.display_name}'s Profile",
            color=discord.Color.blue()
        )
        embed.add_field(name="💰 Gold", value=str(player["gold"]), inline=True)
        embed.add_field(name="🏆 Wins", value=str(player["wins"]), inline=True)
        embed.add_field(name="💀 Losses", value=str(player["losses"]), inline=True)
        
        if player["wins"] + player["losses"] > 0:
            winrate = (player["wins"] / (player["wins"] + player["losses"])) * 100
            embed.add_field(name="📊 Win Rate", value=f"{winrate:.1f}%", inline=False)
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="challenge", description="Challenge another player to a showdown")
    @app_commands.describe(
        opponent="The player you want to challenge",
        character="Your character choice."
    )
    async def challenge(self, interaction: discord.Interaction, opponent: discord.Member, character: str):
        if opponent.id == interaction.user.id:
            await interaction.response.send_message("You can't challenge yourself!", ephemeral=True)
            return
        
        if opponent.bot:
            await interaction.response.send_message("You can't challenge a bot!", ephemeral=True)
            return
        
        if character not in CHARACTERS:
            await interaction.response.send_message(
                f"Invalid character. Choose from: {', '.join(CHARACTERS.keys())}", 
                ephemeral=True
            )
            return
        
        challenge_id = f"{interaction.user.id}_{opponent.id}"
        self.pending_battles[challenge_id] = {
            "challenger": interaction.user.id,
            "opponent": opponent.id,
            "char1": character
        }
        
        embed = discord.Embed(
            title="⚔️ LEWIS BATTLE!",
            description=f"{interaction.user.mention} challenges {opponent.mention} to a showdown!\n\n"
                       f"**Challenger's Character:** {CHARACTERS[character]['emoji']} {character} ({CHARACTERS[character]['class']})",
            color=discord.Color.orange()
        )
        embed.set_footer(text=f"{opponent.display_name}, use /accept to choose your character and start the battle.")
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="accept", description="Accept a battle challenge")
    @app_commands.describe(character="Your character choice.")
    async def accept(self, interaction: discord.Interaction, character: str):
        if character not in CHARACTERS:
            await interaction.response.send_message(
                f"Invalid character! Choose from: {', '.join(CHARACTERS.keys())}", 
                ephemeral=True
            )
            return
        
        challenge = None
        challenge_id = None
        for cid, data in self.pending_battles.items():
            if data["opponent"] == interaction.user.id:
                challenge = data
                challenge_id = cid
                break
        
        if not challenge:
            await interaction.response.send_message("You have no pending challenges!", ephemeral=True)
            return
        
        battle = BattleState(
            challenge["challenger"],
            interaction.user.id,
            challenge["char1"],
            character
        )
        
        view = BattleView(battle, self.player_data)
        embed = view.create_embed()
        
        del self.pending_battles[challenge_id]
        await interaction.response.send_message(
            content=f"<@{challenge['challenger']}> <@{interaction.user.id}> The battle begins!",
            embed=embed,
            view=view
        )
    
    @app_commands.command(name="help", description="Show all available commands")
    async def help_command(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🎮 Lewis Showdown Bot Commands",
            description="Battle in the Lewisverse!",
            color=discord.Color.green()
        )
        
        embed.add_field(
            name="/characters",
            value="View all available characters and their stats.",
            inline=False
        )
        embed.add_field(
            name="/profile",
            value="View your profile and gold.",
            inline=False
        )
        embed.add_field(
            name="/challenge @user [character]",
            value="Challenge another player to a battle",
            inline=False
        )
        embed.add_field(
            name="/accept [character]",
            value="Accept a pending battle challenge",
            inline=False
        )
        embed.add_field(
            name="💰 Currency System",
            value="Winners of battles earn 50-150 gold.",
            inline=False
        )
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(LewisShowdown(bot))