import { useState, useRef, useEffect, type ReactNode } from 'react'

interface Props {
  items: ReactNode[]
  pageHeightMm?: number
  paddingVMm?: number   // 상하
  paddingHMm?: number   // 좌우
  gapMm?: number          // 세로(문제-문제) 간격
  columnGapMm?: number    // 가로(좌우 컬럼) 간격
  maxPerColumn?: number   // 한 컬럼에 들어갈 수 있는 최대 문제 수
  header?: ReactNode
}

interface PageColumn {
  indices: number[]
}

interface Page {
  left: PageColumn
  right: PageColumn
}

const MM_TO_PX = 3.7795  // 96dpi: 1mm = 3.7795px

export function A4AutoLayout({ items, pageHeightMm = 297, paddingVMm = 15, paddingHMm = 10, gapMm = 6, columnGapMm = 6, maxPerColumn = Infinity, header }: Props) {
  const measureRef = useRef<HTMLDivElement>(null)
  const [pages, setPages] = useState<Page[] | null>(null)
  const [heights, setHeights] = useState<number[]>([])

  // 1단계: 숨긴 컨테이너에서 각 문제 높이 측정
  useEffect(() => {
    if (!measureRef.current) return
    const children = measureRef.current.children
    const h: number[] = []
    for (let i = 0; i < children.length; i++) {
      h.push(children[i].getBoundingClientRect().height)
    }
    setHeights(h)
  }, [items])

  // 2단계: 높이 기반으로 페이지/열 분배
  useEffect(() => {
    if (heights.length === 0 || heights.length !== items.length) return

    const colHeightPx = (pageHeightMm - paddingVMm * 2 - 2) * MM_TO_PX
    const gapPx = gapMm * MM_TO_PX
    const result: Page[] = []
    let currentPage: Page = { left: { indices: [] }, right: { indices: [] } }
    let leftUsed = 0
    let rightUsed = 0
    let fillingRight = false

    for (let i = 0; i < items.length; i++) {
      const h = heights[i]
      const gap = fillingRight
        ? (currentPage.right.indices.length > 0 ? gapPx : 0)
        : (currentPage.left.indices.length > 0 ? gapPx : 0)

      if (!fillingRight) {
        const leftFull = currentPage.left.indices.length >= maxPerColumn
        if (!leftFull && leftUsed + gap + h <= colHeightPx) {
          currentPage.left.indices.push(i)
          leftUsed += gap + h
        } else {
          fillingRight = true
          if (rightUsed + h <= colHeightPx && currentPage.right.indices.length < maxPerColumn) {
            currentPage.right.indices.push(i)
            rightUsed += h
          } else {
            result.push(currentPage)
            currentPage = { left: { indices: [i] }, right: { indices: [] } }
            leftUsed = h
            rightUsed = 0
            fillingRight = false
          }
        }
      } else {
        const rightFull = currentPage.right.indices.length >= maxPerColumn
        if (!rightFull && rightUsed + gap + h <= colHeightPx) {
          currentPage.right.indices.push(i)
          rightUsed += gap + h
        } else {
          result.push(currentPage)
          currentPage = { left: { indices: [i] }, right: { indices: [] } }
          leftUsed = h
          rightUsed = 0
          fillingRight = false
        }
      }
    }

    if (currentPage.left.indices.length > 0 || currentPage.right.indices.length > 0) {
      result.push(currentPage)
    }

    setPages(result)
  }, [heights, items.length, pageHeightMm, paddingVMm, gapMm, maxPerColumn])

  const colWidth = `calc((100% - ${columnGapMm}mm) / 2)`

  return (
    <>
      {/* 측정용 숨김 컨테이너 */}
      <div
        ref={measureRef}
        style={{
          position: 'absolute',
          visibility: 'hidden',
          width: `calc((210mm - ${paddingHMm * 2}mm - ${columnGapMm}mm) / 2)`,
          left: '-9999px',
        }}
      >
        {items.map((item, i) => (
          <div key={i}>{item}</div>
        ))}
      </div>

      {/* 실제 페이지 렌더링 */}
      {pages && pages.map((page, pi) => (
        <div key={pi} className="a4-paper">
          {pi === 0 && header && (
            <div style={{ marginBottom: `${gapMm}mm` }}>{header}</div>
          )}
          <div style={{ display: 'flex', gap: `${columnGapMm}mm`, height: '100%' }}>
            <div style={{ width: colWidth }}>
              {page.left.indices.map(i => (
                <div key={i} style={{ marginBottom: `${gapMm}mm` }}>{items[i]}</div>
              ))}
            </div>
            <div style={{ width: colWidth }}>
              {page.right.indices.map(i => (
                <div key={i} style={{ marginBottom: `${gapMm}mm` }}>{items[i]}</div>
              ))}
            </div>
          </div>
        </div>
      ))}
    </>
  )
}
