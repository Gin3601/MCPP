# app/services/all_promot.py

PROMPTS = {
    # ======================================================
    # information
    "information": """
    You will edit an existing product mockup using 4 input images.

    INPUT IMAGE MAPPING (MUST FOLLOW EXACTLY):
    - Image 1: the base product mockup photo (plates + napkins + forks).
    - Image 2: the napkin pattern (apply ONLY to napkins).
    - Image 3: the small plate pattern (apply ONLY to the smaller plates).
    - Image 4: the large plate pattern (apply ONLY to the larger plates).

    CRITICAL RULES (DO NOT BREAK):
    1) Do NOT change the camera angle, composition, background, or object positions in Image 1.
    2) Do NOT add or remove any objects. Keep forks, plates, and napkins exactly as in Image 1.
    3) ONLY change the surface print/design by applying the provided pattern images.
    4) Preserve realistic lighting, shadows, highlights, reflections, and texture from Image 1.
    5) The patterns must be perspective-warped to match item geometry (flat for napkins, circular/spherical warp for plates).
    6) Keep edges clean: print must not spill outside plate rims; follow boundaries precisely.
    7) Do NOT blur the patterns. Keep them crisp, high-resolution, and natural.
    8) All numbers, units, and text MUST be copied EXACTLY as written below. Do NOT paraphrase.
    9) If any overlay text cannot be reproduced exactly, do not add it at all.

    PATTERN APPLICATION:
    A) Napkins:
    - Apply Image 2 pattern ONLY to napkins.
    - Keep folds/creases and shading from Image 1 visible; pattern follows folds naturally.

    B) Small plates:
    - Apply Image 3 pattern ONLY to the smaller plates.
    - Keep plate rim and specular highlights realistic.
    - Center the pattern nicely; avoid awkward cropping.

    C) Large plates:
    - Apply Image 4 pattern ONLY to the larger plates.
    - Keep plate rim and specular highlights realistic.
    - Center the pattern nicely; avoid awkward cropping.
    - Apply realistic spherical warp on plate surfaces; preserve rim highlights from Image 1.

    E-COMMERCE INFOGRAPHIC OVERLAY (Amazon-style):
    Add clean, professional overlays on top of the edited photo. ONLY overlays; do not change the photo.

    TOP BANNER:
    - Add a horizontal banner at the top.
    - Text EXACTLY: "96 PIECES  PACKAGE INCLUDES"
    - Style: bold white modern sans-serif text on a solid black (or very dark) rectangle.

    DIMENSIONS (thin white straight double-arrow lines with centered text):
    - "9 inch" for the large plate group.
    - "7 inch" for the small plate group.
    - "6.5 inch" for the napkins (height reference).
    - "7.3 in" for the forks (length reference).
    Rules:
    - Use straight double-arrow lines.
    - Place each measurement near its item but do not cover important details.

    QUANTITY LABELS (solid black rounded rectangles, white sans-serif text, consistent size/spacing):
    - "24× Dinner Plate" near the large plates.
    - "24× Dessert Plate" near the small plates.
    - "24× Napkins" near the napkins.
    - "24× Forks" near the forks.
    Rules:
    - Put each label directly under/near its corresponding item group.
    - Align labels neatly (grid alignment), evenly spaced.
    - Keep label style identical across all labels.

    STYLE GUIDELINES:
    - Font: clean modern sans-serif (no serif, no script).
    - Text color: white.
    - Label background: solid black with rounded corners.
    - No gradients, no decorative icons, no extra text.

    FINAL VERIFICATION BEFORE OUTPUT:
    - Patterns applied to correct items ONLY (napkins=Image2, small plates=Image3, large plates=Image4).
    - All overlay text matches EXACTLY the provided strings, numbers, and units.
    - Original mockup lighting and realism preserved.
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
  - Left side of the plate: one gold fork placed vertically.
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
    Create a high-quality e-commerce infographic image for a party tableware set, in a clean catalog style.
    INPUT IMAGE USAGE (MUST FOLLOW):
    - Image 1 is the PLATE pattern. Apply it to all plate surfaces.
    - Image 2 is the NAPKIN pattern. Apply it to the napkins.
    CANVAS & LAYOUT:
    - Square 1:1 layout, centered composition.
    - Top: a wide horizontal green banner.
      Add the title text EXACTLY: "High Quality Party Tableware Set"
      Use bold white sans-serif text with a subtle outline for readability.
    - Middle section on a clean white background:
      • left: one large round plate facing front
      • right: a neat stack of square napkins with 3–4 gold forks placed on top
    - Bottom: a wide green strip divided into 4 equal blocks, each with a white circular check icon above a label.
      Labels EXACTLY (left to right):
      1) "Food-grade"
      2) "Leak-proof"
      3) "Recyclable"
      4) "Thick Paper"
    PATTERN APPLICATION REQUIREMENTS:
    - Plates: use Image 1 pattern clearly and accurately; center it; keep it crisp; maintain realistic plate shading/highlights.
    - Napkins: use Image 2 pattern clearly and accurately; keep it crisp; match the napkin perspective.
    - Forks: metallic gold look, realistic highlights. Keep forks separate from patterns (do not print patterns on forks).
    STYLE REQUIREMENTS:
    - Professional e-commerce infographic, clean and minimal.
    - Balanced spacing, aligned elements, no clutter.
    - No extra text beyond the specified title and 4 labels.
    - No logos, no watermarks, no brand names.
    FINAL QUALITY CHECK:
    - The structure must match: top banner + product area + bottom 4 feature blocks.
    - All text must match EXACTLY as provided.
    """.strip(),

    "ground": """
    Create a high-quality overhead (top-down) dinner table scene photo for a party / holiday meal.
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
    - Patterns crisp, centered, natural scale. Do NOT blur.
    - Do NOT add any text, logos, or watermarks.
    STYLE:
    - Realistic lifestyle product photography.
    - No text overlays, no icons, no labels.
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

