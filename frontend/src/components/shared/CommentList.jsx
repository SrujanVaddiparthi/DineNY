// filepath: src/components/shared/CommentList.jsx
export default function CommentList({ comments, s }) {
  if (!comments?.length) return <p className={s.noComments}>No comments yet. Be the first!</p>;
  return (
    <div className={s.commentList}>
      {comments.map((c, i) => (
        <div key={i} className={s.commentItem}>
          <div className={s.avatar}>{(c.author || 'A')[0].toUpperCase()}</div>
          <div className={s.bubble}>
            <div className={s.bubbleHead}>
              <span className={s.author}>{c.author || 'Anonymous'}</span>
              <span className={s.date}>{new Date(c.createdAt).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}</span>
            </div>
            <p className={s.commentText}>{c.text}</p>
          </div>
        </div>
      ))}
    </div>
  );
}
