import type { ProcessBoxBlock, ContentBlock } from '../../ln/problem/l0/types'

interface Props {
  block: ProcessBoxBlock
  renderContentBlock: (block: ContentBlock, index: number) => React.ReactNode
}

export function ProcessBoxRenderer({ block, renderContentBlock }: Props) {
  return (
    <fieldset className="process-box">
      {block.title && <legend>{block.title}</legend>}
      <div className="process-box-content">
        {block.content.map((child, i) => (
          <div key={i}>{renderContentBlock(child, i)}</div>
        ))}
      </div>
    </fieldset>
  )
}
