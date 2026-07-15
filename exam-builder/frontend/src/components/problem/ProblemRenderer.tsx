import type { Problem, ContentBlock } from '../../ln/problem/l0/types'
import { PlaceholderText } from './PlaceholderText'
import { CodeBlockRenderer } from './CodeBlockRenderer'
import { TextChoicesRenderer } from './TextChoicesRenderer'
import { ConditionBoxRenderer } from './ConditionBoxRenderer'
import { ItemBoxRenderer } from './ItemBoxRenderer'
import { ProcessBoxRenderer } from './ProcessBoxRenderer'
import './ProblemRenderer.css'

interface Props {
  problem: Problem
  problemNumber?: number
  showExplain?: boolean
}

export function ProblemRenderer({ problem, problemNumber, showExplain }: Props) {

  const renderContentBlock = (
    block: ContentBlock,
    index: number,
    isFirst: boolean = false,
  ): React.ReactNode => {
    switch (block.type) {
      case 'text': {
        const align = block.align ?? 'left'
        return (
          <div key={index} className={`text-block text-${align}`}>
            {isFirst && problemNumber !== undefined && (
              <span className="problem-number">{problemNumber}. </span>
            )}
            <PlaceholderText text={block.content} />
          </div>
        )
      }

      case 'code':
        return (
          <CodeBlockRenderer
            key={index}
            content={block.content}
            language={block.language}
          />
        )

      case 'image':
        return (
          <div key={index} className={`image-block image-${block.align ?? 'center'}`}>
            <img
              src={block.src}
              style={{ width: `${block.width ?? 40}mm` }}
              alt={block.alt ?? ''}
            />
          </div>
        )

      case 'paragraph':
        return (
          <div key={index} className="paragraph-block">
            {block.blocks.map((child, i) => {
              if (child.type === 'text') {
                return (
                  <span key={i} className={child.align ? `text-${child.align}` : ''}>
                    <PlaceholderText text={child.content} />
                  </span>
                )
              }
              if (child.type === 'image') {
                return (
                  <img
                    key={i}
                    className={`inline-image image-${child.align ?? 'left'}`}
                    src={child.src}
                    style={{ width: `${child.width ?? 40}mm` }}
                    alt={child.alt ?? ''}
                  />
                )
              }
              return null
            })}
          </div>
        )

      case 'text-choices':
        return <TextChoicesRenderer key={index} items={block.items} />

      case 'condition-box':
        return <ConditionBoxRenderer key={index} block={block} />

      case 'item-box':
        return <ItemBoxRenderer key={index} block={block} renderContentBlock={renderContentBlock} />

      case 'process-box':
        return <ProcessBoxRenderer key={index} block={block} renderContentBlock={renderContentBlock} />

      case 'input-sample':
        return (
          <div key={index} className="input-sample">
            <pre>{block.content}</pre>
          </div>
        )

      case 'output-sample':
        return (
          <div key={index} className="output-sample">
            <pre>{block.content}</pre>
          </div>
        )

      case 'io-sample':
        return (
          <div key={index} className="io-sample">
            <div className="io-sample-col">
              <pre>{block.input}</pre>
            </div>
            <div className="io-sample-col">
              <pre>{block.output}</pre>
            </div>
          </div>
        )

      case 'answer-box': {
        const lines = block.lines ?? 6
        return (
          <div key={index} className="answer-box">
            {Array.from({ length: lines }, (_, i) => (
              <div key={i} className="answer-box-line" />
            ))}
          </div>
        )
      }

      default:
        return null
    }
  }

  const blocks = showExplain ? (problem.explain ?? []) : problem.content

  return (
    <div className="problem">
      {problem.id && (
        <div className="problem-origin-id">{problem.id}</div>
      )}
      {showExplain && problemNumber !== undefined && (
        <div className="text-block">
          <span className="problem-number">{problemNumber}. </span>
          {problem.answer && (
            <span className="explain-answer">
              {problem.answer.type === 'choice'
                ? `정답: ${problem.answer.value}`
                : `정답: ${problem.answer.value}`}
            </span>
          )}
        </div>
      )}
      {blocks.map((block, i) =>
        renderContentBlock(block, i, !showExplain && i === 0)
      )}
    </div>
  )
}
