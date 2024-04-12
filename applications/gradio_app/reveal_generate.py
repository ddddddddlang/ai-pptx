import gradio as gr
from config import config
import os
import uuid
SYS_PROMPT_TPL = "你是一名资深的文章撰写专家，可以完成复杂的、长文本的生成工作。"
PROMPT_TPL = """撰写一份标题为《{topic}》的文档。
输出内容样式必须采用以下template样式。
其中##为章节，输出内容中至少要有6个章节标题及下面内容!
其中##为章节，输出内容中至少要有6个章节标题及下面内容!
其中##为章节，输出内容中至少要有6个章节标题及下面内容!：

template:

# 演示标题

## 1.章节标题。（后面要求禁止输出：每个##下面必须有2-5个###。）

### **章节内容**：章节副标题。章节副标题20个字以内的。
- **内容标题**: 内容详述，20个字到100个字。此-必须必须包含加粗的内容标题。
- **内容标题**: 内容详述，20个字到100个字。此-必须必须包含加粗的内容标题。
- **内容标题**: 内容详述，20个字到100个字。此-必须必须包含加粗的内容标题。看内容是否需要此-，否则删除此行。
- **内容标题**: 内容详述，20个字到100个字。此-必须必须包含加粗的内容标题。看内容是否需要此-，否则删除此行。
- **内容标题**: 内容详述，20个字到100个字。此-必须必须包含加粗的内容标题。看内容是否需要此-，否则删除此行。
- ![主题](https://source.unsplash.com/1000x600/?+英文主题)

### **表格章节内容**：章节副标题。表格内容下面不需要增加主题配图。
| title | col1 | col2 |
| --- | --- | --- |
| item1 | 2 | 3 |
| item2 | 5 | 6 |

### **章节内容**：章节副标题。章节副标题20个字以内的。
- **内容标题**: 内容详述，20个字到100个字。此-必须必须包含加粗的内容标题。
- **内容标题**: 内容详述，20个字到100个字。此-必须必须包含加粗的内容标题。
- **内容标题**: 内容详述，20个字到100个字。此-必须必须包含加粗的内容标题。看内容是否需要此-，否则删除此行。
- **内容标题**: 内容详述，20个字到100个字。此-必须必须包含加粗的内容标题。看内容是否需要此-，否则删除此行。
- **内容标题**: 内容详述，20个字到100个字。此-必须必须包含加粗的内容标题。看内容是否需要此-，否则删除此行。
- ![主题](https://source.unsplash.com/1000x600/?+英文主题)

### ![主题](https://source.unsplash.com/1000x600/?+英文主题)

## 2.章节标题（后面要求禁止输出：下面的内容参照上面的模板。每个##下面必须有2-5个###。需要有6个章节标题及下面内容。）"""


def generate_presentation_md(topic):
    gen = config.llm.chat_once(
        prompt=PROMPT_TPL.format(topic=topic),
        system_prompt=SYS_PROMPT_TPL,
        model_name="moonshot-v1-8k",
        temperature=0.1,
    )
    content = ""
    for partial_content in gen:
        content += partial_content

    # 缓存到cache folder中并以随机ID命名
    random_id = uuid.uuid4().hex[:8]
    with open(os.path.join(os.getcwd(), f"{config.cache_folder}/{random_id}.md"), "w", encoding="utf-8") as f:
        f.write(content)
    return content, random_id


def generate_live_link(pid):
    return f"""👇 在线体验链接已生成: 

[点击此处访问在线PPT](http://127.0.0.1:8080/presentation/{pid})"""


def reveal_generator_tab():
    with gr.Tab("在线PPT生成"):
        with gr.Row():
            topic_textbox = gr.Textbox(label="Topic", scale=3)
            random_id_textbox = gr.Textbox(label="内容随机码ID", interactive=False, scale=1)
            generate_md_btn = gr.Button("🤖 AI Generate MD", scale=1)
            generate_link_btn = gr.Button("Generate Live Link", scale=1)

        with gr.Row():
            generated_md = gr.Markdown("👉 点击按钮 [🤖 AI Generate MD] 生成内容")

        generate_md_btn.click(fn=generate_presentation_md, inputs=topic_textbox, outputs=[
                              generated_md, random_id_textbox])

        generate_link_btn.click(fn=generate_live_link,
                                inputs=random_id_textbox, outputs=generated_md)
