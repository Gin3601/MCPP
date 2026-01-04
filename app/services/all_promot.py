# app/services/all_promot.py

PROMPTS = {
    # ======================================================
    # information
    "information": """
    You will edit an existing product mockup using 4 input images.

    INPUT IMAGE MAPPING (MUST FOLLOW EXACTLY):
    - Image 1: the base product mockup photo (plates + napkins + forks). This image defines composition, camera angle, lighting, shadows, and object positions.
    - Image 2: the napkin surface pattern and style reference.
    - Image 3: the small plate surface pattern.
    - Image 4: the large plate surface pattern.

    CRITICAL RULES (DO NOT BREAK):
    1) Do NOT change the camera angle, composition, background, or object positions in Image 1.
    2) Do NOT add or remove any objects. Keep forks, plates, and napkins exactly as in Image 1.
    3) ONLY change the surface print/design by applying the provided pattern images.
    4) Preserve realistic lighting, shadows, highlights, reflections, and texture from Image 1.
    5) The patterns must be perspective-warped to match item geometry:
      - Napkins: flat fabric warp following folds.
      - Plates: circular / spherical surface warp.
    6) Keep edges clean: print must not spill outside plate rims; follow boundaries precisely.
    7) Do NOT blur the patterns. Keep them crisp, high-resolution, and natural.
    8) All numbers, units, and text MUST be copied EXACTLY as written below. Do NOT paraphrase.
    9) If any overlay text cannot be reproduced exactly, do not add it at all.

    PATTERN APPLICATION:
    A) Napkins:
    - Apply Image 2 pattern ONLY to napkins.
    - Keep folds, creases, and shading from Image 1 visible; pattern follows folds naturally.

    B) Small plates:
    - Apply Image 3 pattern ONLY to the smaller plates.
    - Keep plate rim and specular highlights realistic.
    - Center the pattern nicely; avoid awkward cropping.

    C) Large plates:
    - Apply Image 4 pattern ONLY to the larger plates.
    - Keep plate rim and specular highlights realistic.
    - Center the pattern nicely; avoid awkward cropping.
    - Apply realistic spherical warp on plate surfaces; preserve rim highlights from Image 1.

    STYLE CONTROL:
    - Do NOT invent new colors, themes, or decorative elements.
    - The overall visual style must be derived strictly from Images 2, 3, and 4.
    - Maintain consistent style across napkins, plates, and all overlays.

    E-COMMERCE INFOGRAPHIC OVERLAY:
    Add clean, professional Amazon-style overlays on top of the edited photo.
    ONLY add overlays; do not change the photo itself.

    LAYOUT BACKGROUND RULE:
    - The main canvas/background must remain clean white (pure or near-white), like a typical Amazon infographic.
    - ONLY the TOP BANNER area may use a colored or dark background rectangle.
    - Do NOT add any other large colored background panels.

    TOP BANNER:
    - Add a horizontal banner at the top.
    - The banner background color/style must be derived from Images 2–4 so it visually matches the product theme.
    - Text EXACTLY:
    "96 PIECES  PACKAGE INCLUDES"
    - Style: bold white modern sans-serif text on a solid dark rectangle.

    DIMENSIONS (DISPLAY TEXT ONLY — DO NOT MEASURE):
    - Add thin white straight double-arrow lines with centered text.
    - Display these EXACT texts (do NOT calculate or change values):
      - "9 inch" for the large plate group.
      - "7 inch" for the small plate group.
      - "6.5 inch" for the napkins (height reference).
      - "7.3 in" for the forks (length reference).
    - Place each measurement near its item without covering important details.

    QUANTITY LABELS:
    - Add compact rounded rectangles with white modern sans-serif text.
    - Label background color/style must be dark and derived from Images 2–4, suitable for white text.
    - Use EXACT texts:
      - "24× Dinner Plate" near the large plates.
      - "24× Dessert Plate" near the small plates.
      - "24× Napkins" near the napkins.
      - "24× Forks" near the forks.
    - Put each label directly under or near its corresponding item group.
    - Align labels neatly (grid alignment), evenly spaced.
    - Keep all labels identical in size, shape, and style.
    - Labels must remain compact and must not expand into large background blocks.

    STYLE GUIDELINES:
    - Font: clean modern sans-serif (no serif, no script).
    - Text color: white.
    - No gradients, no decorative icons, no extra text.

    FINAL VERIFICATION BEFORE OUTPUT:
    - Patterns applied to correct items ONLY (napkins=Image2, small plates=Image3, large plates=Image4).
    - All overlay text matches EXACTLY the provided strings, numbers, and units.
    - Original mockup lighting and realism are fully preserved.
    - Top banner has a colored/dark background; all other areas remain clean white.

    """.strip(),
    # ======================================================
    # bigplate
    "bigplate": """
    Create a high-quality e-commerce infographic image for disposable party tableware.
  INPUT IMAGE USAGE:
  - Image 1: use this as the LARGE plate surface pattern.
  - Image 2: use this as the napkin surface pattern.

  LAYOUT & STRUCTURE:
  - Square 1:1 canvas.
  - Neutral warm background (light beige / cream tone).
  - Center-left: one large round plate facing forward.
  - On top of the plate: a neatly placed square napkin using the napkin pattern.
  - Left side of the plate: one fork placed vertically.
  - Add a small green plant or subtle decorative element on the right side for balance.

  TOP LABEL:
  - Top-left corner: a white rectangular label.
  - Text EXACTLY: "Metal dots design"
  - Black clean sans-serif font.

  PATTERN APPLICATION:
  - Apply Image 1 pattern clearly and accurately to the large plate.
  - Apply Image 2 pattern clearly and accurately to the napkin.
  - Patterns must be crisp, centered, and scaled naturally.
  - Plate should have realistic depth, highlights, and shadows.
  - Napkin should look soft and layered.

  BOTTOM FEATURE ICONS & TEXT:
  Place features along the bottom area with simple icons and text:
  - "Not easy to fall off"
  - "Highly absorbent"
  - "Soft and comfortable"
  - A round badge with text EXACTLY: "PARABEN FREE"

  STYLE REQUIREMENTS:
  - Professional product photography style.
  - Clean, balanced composition.
  - No extra text beyond what is specified.
  - No logos, no watermarks, no brand names.

  FINAL QUALITY:
  - Image should look like a premium e-commerce product image.
  - Clear focus on the plate and napkin patterns.

    """.strip(),
    # ======================================================
    # smallplate
    "smallplate": """
    Create a high-quality e-commerce infographic image for the banquet tableware collection in a clean catalog style.
    Input image usage (must follow) :
    Figure 1 shows the PLATE pattern.  Apply it to all board surfaces.
    Figure 2 shows the pattern of the napkin.  Spread it on the napkin.
    Canvas and layout
    - Square 1:1 layout, centered composition.
    - Top: A wide horizontal banner consistent with the theme of the uploaded image.
    Add title text: "High-Quality Banquet Tableware Set"
    Use bold white sans-serif text with fine Outlines to enhance readability.
    The middle part is on a clean white background;
    • Left: A large round plate faces forward
    On the right: A neat stack of square napkins with 3 to 4 gold forks placed on top
    - Bottom:  A wide strip of the theme of the uploaded image , divided into 4 equal blocks, each with a white circular checkmark on top.
    Accurate labels (from left to right) :
    "Food grade”
    2) "Leak“
    3) "Recyclable”
    4) "Thick paper”
    Pattern application requirements
    - Board: Use the pattern in Figure 1 clearly and accurately;  Center Stay crispy;  Maintain the true board shadows/highlights.
    - Napkins: Use the pattern in Figure 2 clearly and accurately;  Stay crispy;  Match the Angle of the napkin.
    - Fork: A disposable appearance consistent with the theme, a realistic highlight.  Separate the fork from the pattern (do not print the pattern on the fork).
    Style requirements
    Professional e-commerce infographics, clean and minimal.
    Balanced spacing, aligned elements, no clutter.
    There is no additional text except for the specified title and four tags.
    - No trademarks, no watermarks, no brand names.
    Final quality inspection
    The structure must match: the top banner + the product area + the four functional blocks at the bottom.
    All the text must exactly match what is provided.
    """.strip(),
    # ======================================================  
    "ground": """
    Create a high-quality overhead (top-down) dinner table scene 1:1photo for a party / holiday meal.
    INPUT IMAGE USAGE (MUST FOLLOW EXACTLY):
    - Image 1: use this as the LARGE disposable dinner plate pattern.
    - Image 2: use this as the SMALL disposable dessert plate pattern.
    - Image 3: use this as the disposable napkin pattern.
    SCENE REQUIREMENTS:
    - Camera angle: perfectly top-down / overhead view of a wooden dining table.
    - The table is fully set for multiple guests (8–10 place settings).
    - Include BOTH plate sizes in the scene:
    • Large dinner plates (use Image 1 pattern) at each place setting.
    • Small dessert plates (use Image 2 pattern) at some place settings or near desserts.
    - Include napkins at every place setting (use Image 3 pattern), folded neatly, placed on top of plates or beside plates.
    - Include gold disposable cutlery placed neatly.
    - Include realistic food dishes and drinks, similar to a festive table.
    - Photorealistic lighting and shadows.
    PATTERN ACCURACY (VERY IMPORTANT):
    - Patterns must be applied clearly and accurately, not replaced by other designs.
    - Patterns crisp, centered, natural scale.   Do NOT blur.
    - Do NOT add any text, logos, or watermarks.
    STYLE:
    - Realistic lifestyle product photography.
    - No text overlays, no icons, no labels.
    """.strip(),
    # ======================================================
    # ground2
    "ground2": """
    Please take the pattern picture I uploaded as the sole and final source of the printed texture.
    The pattern content must remain 100% original and no design changes of any form are allowed, including but not limited to:
    No redrawing, no color change, no re-arrangement, no alteration of proportion, no change of line thickness, no alteration of text content or font, and no addition or deletion of any pattern elements are allowed.
    Patterns can only be understood as completed printed pattern resources, rather than design elements that can be recreated.
    The use of patterns is limited to printing textures in the real world
    Only the pattern is allowed to be adhered to the surface of the paper plate and/or napkin in a realistic printing effect.
    Only necessary perspective bending, realistic physical light and shadow, and slight paper and printing grain texture are allowed.
    Any illustration, cartoonization, stylization, 3D rendering, toy-like texture or virtual material presentation is strictly prohibited.
    The final image must be a realistic photography of an e-commerce product in the real world, rather than a concept drawing or design drawing. The specific requirements are as follows:
    Use a white or light-colored tablecloth or desktop with real fabric or desktop texture
    A circular paper plate is placed in the cente
    The pattern is truly printed on the surface of the paper plate
    Place solid-colored tableware of a color similar to the theme on the paper plate
    A square napkin is placed under the paper plate, and the surface of the napkin is also printed with the same pattern realistically
    A few golden scraps of paper are naturally dotted on the desktop
    A few random small decorative items may appear at the edge of the desktop, but they must not cover the main body of the patterns and text
    The photography style must be:
    Natural soft light, high resolution, clear focus, true shadows, clean composition, standard e-commerce product photography.
    The following situations are regarded as incorrect results once they occur and must be avoided:
    The patterns are redesigned, colored, rearranged, repainted or stylized
    The text content is incorrect, missing, mirrored, garbled or replaced
    It presents a cartoonish, illustrative, 3D, rendered or toy-like texture
    Characters, hands, brand logos, watermarks and signatures appear
    The picture is blurry, with low clarity, excessive blurring or severe noise
    Please strictly abide by all the above rules when generating images.
""".strip(),
    # ======================================================
    # main
    "main": """
    你将收到 4 张图片：
    - images[0]: 示例编辑图（四件套电商图，白底，包含：左上纸巾、右上叉子、左下6寸盘、右下9寸盘）——这是必须被编辑输出的基底图(canvas)
    - images[1]: 花纹图1（必须原样保持，不可重绘/风格化/重新解释）
    - images[2]: 花纹图2（必须原样保持，不可重绘/风格化/重新解释）
    - images[3]: 花纹图3（必须原样保持，不可重绘/风格化/重新解释）
    任务：精确贴图替换（exact texture replacement），不是重新设计。
    在保持 images[0] 的布局、物体位置、比例、光影、清晰度、背景完全不变的情况下，只做表面印刷图案替换：
    1) 将 images[1] 的花纹【原样】贴到 images[0] 左上角物体“纸巾”表面。
    2) 将 images[2] 的花纹【原样】贴到 images[0] 左下角物体“6寸餐盘”表面。
    3) 将 images[3] 的花纹【原样】贴到 images[0] 右下角物体“9寸餐盘”表面。
    严格规则（必须遵守）：
    - 花纹必须与输入完全一致：颜色、元素、文字、排版都不能变
    - 不得重绘、不得风格化、不得“参考后重做”、不得生成相似图案
    - 不裁剪、不拉伸、不旋转、不改比例；保持花纹原始布局
    - 只替换物体表面纹理：不能改变物体形状、位置、数量、阴影、反光、边缘
    - 背景保持纯白，输出亚马逊风格 1:1 电商产品图
    输出：一张与 images[0] 同构图的白底1:1产品图，完成三处贴图替换。
    """.strip(),




}

def get_prompt(name: str) -> str:
    try:
        return PROMPTS[name]
    except KeyError:
        raise RuntimeError(f"❌ Prompt '{name}' not found in all_promot.py")

