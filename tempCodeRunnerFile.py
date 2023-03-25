if len(str(log_text_box.get("1.0", "end-1c"))) and len(user):
               logging.info(f'{user[0]}: "{log_text_box.get("1.0", "end-1c")}"')
               log_text_box.delete("1.0","end")