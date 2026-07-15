import { MARKERS } from '../../ln/problem/l0/types'
import type { ConditionBoxBlock } from '../../ln/problem/l0/types'
import { PlaceholderText } from './PlaceholderText'

interface Props {
  block: ConditionBoxBlock
}

export function ConditionBoxRenderer({ block }: Props) {
  const markers = MARKERS[block.marker ?? 'kr-con-rb']

  return (
    <fieldset className="condition-box">
      {block.title && <legend>{block.title}</legend>}
      <div className="condition-items">
        {block.items.map((item, i) => (
          <div key={i} className="condition-item">
            <span className="item-marker">{markers[i]}</span>
            <PlaceholderText text={item} />
          </div>
        ))}
      </div>
    </fieldset>
  )
}
