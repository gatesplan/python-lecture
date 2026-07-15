import { describe, it, expect } from 'vitest'
import { parsePlaceholders } from '../../../../src/ln/problem/l0/parsePlaceholders'

describe('parsePlaceholders', () => {
  it('placeholder가 없는 문자열은 segment 하나, blanks 빈 배열', () => {
    const result = parsePlaceholders('print("hello")')
    expect(result.segments).toEqual(['print("hello")'])
    expect(result.blanks).toEqual([])
  })

  it('빈 문자열', () => {
    const result = parsePlaceholders('')
    expect(result.segments).toEqual([''])
    expect(result.blanks).toEqual([])
  })

  it('placeholder 하나를 파싱한다', () => {
    const result = parsePlaceholders('return [[1]]')
    expect(result.segments).toEqual(['return ', ''])
    expect(result.blanks).toEqual([
      { index: 0, label: '1' },
    ])
  })

  it('placeholder 여러 개를 순서대로 파싱한다', () => {
    const result = parsePlaceholders('if [[조건]]:\n    return [[결과]]')
    expect(result.segments).toEqual(['if ', ':\n    return ', ''])
    expect(result.blanks).toEqual([
      { index: 0, label: '조건' },
      { index: 1, label: '결과' },
    ])
  })

  it('연속된 placeholder를 처리한다', () => {
    const result = parsePlaceholders('[[가]][[나]]')
    expect(result.segments).toEqual(['', '', ''])
    expect(result.blanks).toEqual([
      { index: 0, label: '가' },
      { index: 1, label: '나' },
    ])
  })

  it('빈 label의 placeholder를 처리한다', () => {
    const result = parsePlaceholders('x = [[]]')
    expect(result.segments).toEqual(['x = ', ''])
    expect(result.blanks).toEqual([
      { index: 0, label: '' },
    ])
  })

  it('대괄호 하나는 placeholder로 인식하지 않는다', () => {
    const result = parsePlaceholders('arr[0] = [1, 2]')
    expect(result.segments).toEqual(['arr[0] = [1, 2]'])
    expect(result.blanks).toEqual([])
  })

  it('segments.length === blanks.length + 1 항상 성립', () => {
    const cases = [
      '',
      'no blanks',
      '[[1]]',
      'a[[1]]b',
      '[[1]][[2]][[3]]',
      'start[[a]]mid[[b]]end',
    ]
    for (const input of cases) {
      const result = parsePlaceholders(input)
      expect(result.segments.length).toBe(result.blanks.length + 1)
    }
  })
})
