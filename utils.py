
import fitz  # PyMuPDF
import io

def steganographic_prompt_line(pdf_bytes, hidden_text, x_fraction=0.1, y_fraction=0.1, width_fraction=0.6, rgb_color=(0, 0, 0)):
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    font_size = 3.0
    bar_height = 3

    for page in doc:
        width = page.rect.width
        height = page.rect.height

        x = width * x_fraction
        y = height * y_fraction
        bar_width = width * width_fraction

        # Draw the bar with user-defined color
        rect = fitz.Rect(x, y, x + bar_width, y + bar_height)
        page.draw_rect(rect, color=rgb_color, fill=rgb_color, overlay=True)

        # Insert invisible OCR-readable prompt just below the bar
        page.insert_text(
            (x + 4, y + bar_height + 3),
            hidden_text,
            fontsize=font_size,
            fontname="courier",
            color=(1, 1, 1),
            render_mode=3,
            overlay=True
        )

    out = io.BytesIO()
    doc.save(out)
    doc.close()
    return out.getvalue()

def invisible_prompt(pdf_bytes, hidden_text):
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    font_size = 3.0
    y = 30
    for page in doc:
        page.insert_text((4, y), hidden_text, fontsize=font_size, fontname="courier",
                         color=(1, 1, 1), render_mode=3, overlay=True)
    out = io.BytesIO()
    doc.save(out)
    doc.close()
    return out.getvalue()

def add_alt_text_prompt(pdf_bytes, hidden_text):
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    page = doc[0]
    rect = fitz.Rect(50, 50, 150, 150)

    page.insert_text((rect.x0, rect.y1 + 6), hidden_text,
                     fontsize=2,
                     fontname="courier",
                     color=(1, 1, 1),
                     render_mode=3,
                     overlay=True)

    out = io.BytesIO()
    doc.save(out)
    doc.close()
    return out.getvalue()

def extract_text_for_ai_preview(pdf_bytes):
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    return "\n".join(page.get_text() for page in doc).strip()
