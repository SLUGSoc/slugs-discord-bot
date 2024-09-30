from discord import Colour, TextChannel, Message, Member, Embed

from src.interactions.gauth import get_totp_token

class MessageTemplates:
    attach_str = "This log entry exceeds the Discord character limit, and has been attached as a text file."

    @staticmethod
    def template_wrapper(func):
        def template(*args, **kwargs) -> Embed:
            header, message, footer, colour = func(*args, **kwargs)
            if len(message) >= 4096:
                message = message[:4093] + "..."
            embed = Embed(colour=colour, title=f"`{header}`", description=message)
            embed.set_footer(text=footer)
            return embed
        return template


    @staticmethod
    @template_wrapper
    def edit(pre_message: Message, post_message: Message) -> (str, str, str, Colour):
        edit_header = f"MESSAGE EDITED"
        edit_string = (
            f'The following message by **{post_message.author.name}** was edited in {post_message.channel.mention}.\n' +
            f'**Before:**\n{pre_message.content}\n**After:**\n{post_message.content}\n'
        )
        edit_footer = f"Message ID: {post_message.id}"
        return edit_header, edit_string, edit_footer, Colour.yellow()

    @staticmethod
    @template_wrapper
    def edit_raw(message_id: int, channel: TextChannel) -> (str, str, str, Colour):
        edit_header = "MESSAGE EDITED"
        edit_string = (
            f'A message was edited in {channel.mention}, but could not be retrieved from the message cache.\n'
        )
        edit_footer = f"Message ID: {message_id}"
        return edit_header, edit_string, edit_footer, Colour.yellow()

    @staticmethod
    @template_wrapper
    def delete(message: Message) -> (str, str, str, Colour):
        delete_header = "MESSAGE DELETED"
        delete_string = (
                f"The following message from **{message.author.name}** was deleted from {message.channel.mention}:\n" +
                f"{message.content}"
        )
        delete_footer = f"Message ID: {message.author.id}"
        return delete_header, delete_string, delete_footer, Colour.red()

    @staticmethod
    @template_wrapper
    def delete_raw(message_id: int, channel: TextChannel) -> (str, str, str, Colour):
        delete_header = "MESSAGE DELETED"
        delete_string = (
            f'A message was deleted from {channel.mention}, but could not be retrieved from the message cache.\n'
        )
        delete_footer = f"Message ID: {message_id}"
        return delete_header, delete_string, delete_footer, Colour.red()

    @staticmethod
    @template_wrapper
    def member_leave(member: Member) -> (str, str, str, Colour):
        leave_header = f"USER LEFT"
        leave_string = f'**{member.name}** has left the server.'
        leave_footer = f"User ID: {member.id}"
        return leave_header, leave_string, leave_footer, Colour.dark_red()

    @staticmethod
    @template_wrapper
    def member_leave_raw() -> (str, str, str, Colour):
        leave_header = f"USER LEFT"
        leave_string = f'A user has left the server, but no user details could be recovered from the member cache.'
        leave_footer = ""
        return leave_header, leave_string, leave_footer, Colour.dark_red()

    @staticmethod
    @template_wrapper
    def auth_message(secrets: list[dict[str, str]]) -> (str, str, str, Colour):
        auth_header = "Google Auth Codes"
        auth_string = ""
        for service in secrets:
            auth_string += f"**{service["name"]}**: {get_totp_token(service["secret"])}\n"
        auth_footer = "*This message will self-destruct after 30 seconds...*"
        return auth_header, auth_string, auth_footer, Colour.pink()
