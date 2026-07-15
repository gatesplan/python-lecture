import { describe, it, expect } from 'vitest'
import { validateProblem } from '../../../../src/ln/problem/l1/validateProblem'
import type { Problem } from '../../../../src/ln/problem/l0/types'

describe('validateProblem', () => {
  // --- 유효한 문제 ---

  it('최소 유효 문제 (text 블록 하나)', () => {
    const p: Problem = {
      type: 'short',
      content: [{ type: 'text', content: '1+1=?' }],
    }
    expect(validateProblem(p)).toEqual({ valid: true, errors: [] })
  })

  it('객관식 문제 (text + text-choices + answer)', () => {
    const p: Problem = {
      type: 'select',
      content: [
        { type: 'text', content: '다음 중 옳은 것은?' },
        { type: 'text-choices', items: ['A', 'B', 'C', 'D', 'E'] },
      ],
      answer: { type: 'choice', value: 3 },
    }
    expect(validateProblem(p)).toEqual({ valid: true, errors: [] })
  })

  it('코드 블록 + io-sample이 포함된 문제', () => {
    const p: Problem = {
      type: 'short',
      content: [
        { type: 'text', content: '출력을 작성하시오.' },
        { type: 'code', content: 'print(1+2)', language: 'python' },
        { type: 'io-sample', input: '없음', output: '3' },
      ],
    }
    expect(validateProblem(p)).toEqual({ valid: true, errors: [] })
  })

  // --- type 검증 ---

  it('type이 없으면 실패', () => {
    const p = { content: [{ type: 'text', content: 'hi' }] } as any
    const result = validateProblem(p)
    expect(result.valid).toBe(false)
    expect(result.errors.some(e => e.includes('type'))).toBe(true)
  })

  it('type이 유효하지 않으면 실패', () => {
    const p = { type: 'essay', content: [{ type: 'text', content: 'hi' }] } as any
    const result = validateProblem(p)
    expect(result.valid).toBe(false)
    expect(result.errors.some(e => e.includes('type'))).toBe(true)
  })

  // --- content 검증 ---

  it('content가 없으면 실패', () => {
    const p = { type: 'short' } as any
    const result = validateProblem(p)
    expect(result.valid).toBe(false)
    expect(result.errors.some(e => e.includes('content'))).toBe(true)
  })

  it('content가 빈 배열이면 실패', () => {
    const p: Problem = { type: 'short', content: [] }
    const result = validateProblem(p)
    expect(result.valid).toBe(false)
    expect(result.errors.some(e => e.includes('content'))).toBe(true)
  })

  it('알 수 없는 블록 type이면 실패', () => {
    const p = {
      type: 'short',
      content: [{ type: 'unknown-block', content: 'x' }],
    } as any
    const result = validateProblem(p)
    expect(result.valid).toBe(false)
    expect(result.errors.some(e => e.includes('unknown-block'))).toBe(true)
  })

  // --- 블록별 필수 필드 ---

  it('text 블록에 content가 없으면 실패', () => {
    const p = {
      type: 'short',
      content: [{ type: 'text' }],
    } as any
    const result = validateProblem(p)
    expect(result.valid).toBe(false)
  })

  it('code 블록에 content가 없으면 실패', () => {
    const p = {
      type: 'short',
      content: [{ type: 'code' }],
    } as any
    const result = validateProblem(p)
    expect(result.valid).toBe(false)
  })

  it('text-choices에 items가 빈 배열이면 실패', () => {
    const p: Problem = {
      type: 'select',
      content: [
        { type: 'text', content: '?' },
        { type: 'text-choices', items: [] },
      ],
    }
    const result = validateProblem(p)
    expect(result.valid).toBe(false)
  })

  it('io-sample에 input 또는 output이 없으면 실패', () => {
    const p = {
      type: 'short',
      content: [
        { type: 'text', content: '?' },
        { type: 'io-sample', input: 'x' },
      ],
    } as any
    const result = validateProblem(p)
    expect(result.valid).toBe(false)
  })

  // --- answer 검증 ---

  it('answer.type이 유효하지 않으면 실패', () => {
    const p = {
      type: 'short',
      content: [{ type: 'text', content: '?' }],
      answer: { type: 'multi', value: [1, 2] },
    } as any
    const result = validateProblem(p)
    expect(result.valid).toBe(false)
    expect(result.errors.some(e => e.includes('answer'))).toBe(true)
  })

  it('answer가 없어도 유효 (answer는 optional)', () => {
    const p: Problem = {
      type: 'explain',
      content: [{ type: 'text', content: '서술하시오.' }],
    }
    expect(validateProblem(p)).toEqual({ valid: true, errors: [] })
  })
})
