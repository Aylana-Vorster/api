 


def draw_text(draw_obj, text, position, font_obj, max_width, max_height):
        words = text.split()
        lines = []
        current_line = words.pop(0)
        
        for word in words:
            test_line = current_line + " " + word
            if draw_obj.textbbox(position, test_line, font=font_obj)[2] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word

        lines.append(current_line)

        # Calculate total height of the text block
        total_height = sum([draw_obj.textbbox(position, line, font=font_obj)[3] for line in lines])

        # Calculate starting y position for centering
        y = position[1] + (max_height - total_height) // 2

        for line in lines:
            # Calculate x position for centering
            x = position[0] + (max_width - draw_obj.textbbox(position, line, font=font_obj)[2]) // 2
            draw_obj.text((x, y), line, font=font_obj, fill="white")
            y += draw_obj.textbbox(position, line, font=font_obj)[3]
