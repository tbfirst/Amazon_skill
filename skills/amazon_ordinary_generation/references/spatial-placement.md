# 空间、摆放与透视

场景、场景型A+及含环境的细节图必读。把产品相对房间的摆放与相机视角分别决定，不能只写“three-quarter view”或“realistic perspective”。

## 每图空间蓝图

记录 supportPlane（地面/台面/墙面）、roomAxes（墙脚线/地板接缝/桌沿）、productOrientation、cameraView、contactPoints、clearance、scaleBasis、lightDirection。真实尺寸来自本SKU；具体机位和空隙是设计提案，不假称从竞品图测得。

- 靠墙的方形柜体、狗笼或收纳箱，默认背面与所靠墙面平行，底面稳定落在支撑平面；说明背面留有合理空隙，四角不穿墙、不悬空。侧面与背面保持产品真实角度。贴墙不是所有商品的通用规则，按用途确定。
- 想展示正面和侧面时，移动相机到前侧方；产品仍维持已定摆放。只有明确需要斜放且有足够空间时才旋转商品，并交代旋转后背角与墙的空隙。桌面卡套、穿戴物等沿实际支撑和操作确定朝向，不机械套柜体规则。
- 同一场景使用一致的地平线与透视投影；空间中平行的边缘在画面上应遵循同组消失点关系，不能强求透视边在像素上平行。不同实体朝向可以有不同消失点，但必须属于同一视点。避免产品是俯视、房间却是平视的拼贴。
- 比例参照优先用已知尺寸且深度相近的物件；远处窗户、前景狗和商品不可直接按像素比较。未知镜头参数不编造为证据；必要时采用弱透视、较正面的保守设计，不拉伸产品修复空间。
- 接触点、接触影、投影与主光一致。开门、抽屉、折板有真实运动空间；所有道具与动物同时服从地面、净空、遮挡顺序和重力。产品轮廓及关键功能可辨，不能用装饰遮住穿帮。

英文prompt独立写清实际关系，例如：
“Keep the cabinet stationary with its rear face parallel to the wall and its base resting squarely on the floor. Move the camera to a front-side viewpoint to reveal the front and side; do not rotate the cabinet diagonally relative to the wall. Maintain one coherent room perspective, a clear rear-wall gap, grounded contact shadows, and unobstructed door clearance.”

仅将适用部分改为当前SKU，不能给非柜体商品直接套此示例。交付前核对源参考→空间蓝图→prompt；实际出图后检查墙脚线、产品边、落地角点、尺度与阴影，纯文字检查不能证明渲染已正确。
