import io

from discord import TextChannel, File, Message, User, Member


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
            f'The following message by **{post_message.author}** was edited in {channel.mention}.\n' +
            f'**Before:**\n{pre_message.content}\n**After:**\n{post_message.content}\n'
        )
        return edit_header, edit_string

    @staticmethod
    @template_wrapper
    def edit_raw(message_id: int, channel: TextChannel) -> (str, str):
        edit_header = f'>>> ```css\n"MESSAGE EDITED" "Message ID:" {message_id}```"\n'

        edit_string = (
            f'A message was edited in {channel.mention}, but could not be retrieved from the message cache.\n'
        )
        return edit_header, edit_string

    @staticmethod
    @template_wrapper
    def delete(message: Message) -> (str, str):
        delete_header = f'>>> ```css\n[MESSAGE DELETED] [Message ID:] {message.id} [User ID:] {message.author.id}```\n'

        delete_string = (
                f"The following message from **{message.author.name}** was deleted from {message.channel.mention}:\n" +
                f"*{message.content}*"
        )
        return delete_header, delete_string

    @staticmethod
    @template_wrapper
    def delete_raw(message_id: int, channel: TextChannel) -> (str, str):
        delete_header = f'>>> ```css\n[MESSAGE DELETED] [Message ID:] {message_id}```'

        delete_string = (
            f'A message was deleted from {channel.mention}, but could not be retrieved from the message cache.\n'
        )
        return delete_header, delete_string

    @staticmethod
    @template_wrapper
    def member_leave(member: Member) -> (str, str):
        leave_header = f'>>> ```ini\n[USER LEFT] [User ID:] {member.id}```\n'
        leave_string = f'{member.name} has left the server.'
        return leave_header, leave_string

    @staticmethod
    @template_wrapper
    def member_leave_raw() -> (str, str):
        leave_header = f'>>> ```ini\n[USER LEFT]```\n'
        leave_string = f'A user has left the server, but no user details could be recovered from the member cache.'
        return leave_header, leave_string
