import io

from discord import TextChannel, File, Message, User

from main import client

class MessageTemplates:
    attach_str = "This log entry exceeds the Discord character limit, and has been attached as a text file."

    @staticmethod
    def template_wrapper(func):
        def template(*args, **kwargs) -> tuple[str, File | None]:
            header, message = func(*args, **kwargs)
            if len(whole_str := header + message) >= 2000:
                return_str = header + MessageTemplates.attach_str
                attachment = File(io.BytesIO(whole_str))
            else:
                return_str = whole_str
                attachment = None
            return return_str, attachment
        return template


    @staticmethod
    @template_wrapper
    def edit(pre_message: Message, post_message: Message, channel: TextChannel) -> (str, str):
        edit_header = f'>>> ```css\n"MESSAGE EDITED" "Message ID:" {post_message.id}```"\n'

        edit_string = (
            f'The following message by **{post_message.author}** was edited in {channel.name}.\n' +
            f'**Before:**\n{pre_message.content}\n**After:**\n{post_message.content}\n'
        )
        return edit_header, edit_string

    @staticmethod
    @template_wrapper
    def delete(cached_msg: Message | None, channel: TextChannel) -> (str, str):
        delete_header = f'>>> ```css\n[MESSAGE DELETED] [Message ID:] {cached_msg.id or "N/A"}```'

        if cached_msg:
            delete_string = (
                f"[User ID:] {cached_msg.author.id}```\n" +
                f"The following message from **{cached_msg.author}** was deleted from {channel.name}:\n" +
                f"*{cached_msg.content}*"
            )
        else:
            delete_string = (
                f"*A message was deleted from {channel.name}, but could not be found in the message cache.*"
            )
        return delete_header, delete_string

    @staticmethod
    @template_wrapper
    def member_leave(user: User) -> (str, str):
        leave_header = f'>>> ```ini\n[USER LEFT] [User ID:] {user.id}```\n'
        leave_string = f'{user.name} has left the server.'
        return leave_header, leave_string

@client.event
async def on_message_edit(before: Message, after: Message):
    channel = after.channel
    msg_str, attach = MessageTemplates.edit(before, after)
    await channel.send(msg_str, file=attach)
