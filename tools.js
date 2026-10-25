/**
 * UTILITY NEXUS service registry.
 * Add new objects to this array to publish more tools (no HTML edits needed).
 * Only public HTTPS destinations should be registered.
 * Categories: media, file, productivity, developer, other.
 */
window.UTILITY_TOOLS = Object.freeze([
  {
    id: 'imgcomp',
    name: 'Imgcomp',
    subtitle: '로컬 이미지 · 동영상 중복 정리실',
    description: '흩어진 사진과 동영상의 중복을 검색하고 비교하세요. 남길 원본은 직접 선택하고, 삭제하기 전에 다시 확인할 수 있습니다.',
    category: ['media', 'file'],
    tags: ['중복 검색', '이미지 · 동영상', '로컬 처리'],
    url: 'https://imgcomp.moip.ai.kr/',
    repository: 'https://github.com/teamprotofelix/Imgcomp',
    image: './assets/imgcomp-media.webp',
    imageAlt: '디지털 이미지와 동영상 파일을 비교하는 홀로그램 카드 일러스트',
    status: 'live',
    featured: true,
  },
]);
