import { MARKERS } from '../../ln/problem/l0/types'
import type { ItemBoxBlock, ContentBlock } from '../../ln/problem/l0/types'

interface Props {
  block: ItemBoxBlock
  renderContentBlock: (block: ContentBlock, index: number) => React.ReactNode
}

export function ItemBoxRenderer({ block, renderContentBlock }: Props) {
  const markers = block.marker ? MARKERS[block.marker] : null

  return (
    <fieldset className="item-box">
      {block.title && <legend>{block.title}</legend>}
      <div className="item-box-items">
        {block.items.map((item, i) => (
          <div key={i} className="item-box-item">
            {markers && <span className="item-marker">{markers[i]}</span>}
            <div className="item-box-content">
              {renderContentBlock(item as ContentBlock, i)}
            </div>
          </div>
        ))}
      </div>
    </fieldset>
  )
}
