"""Plans from the end of each lesson's main line: what to aim for once the moves you know run out.

Keys are lesson ids from either book. Each plan has a headline (h) and bullets (b) of (kind, text), where kind is
king, pawns, pieces, target, them or watch. Written from the final position of the main line and checked against
Stockfish's continuation from there. No notation: the squares f7 and f2 are the only ones ever named.
Lines that end in mate need no plan and have none.
"""

W = {
  # ---------------------------------------------------------------- the Italian
  'setup': dict(h='Small pawn, big center, castle', b=[
    ('pawns', 'Next comes the small c-pawn move, then the d-pawn two squares: two pawns side by side in the middle.'),
    ('king', 'Castle short early. The rook then comes to the e-file behind your center.'),
    ('target', 'f7. Only the king guards it, and your bishop already points at it.'),
    ('them', 'Black copies your bishop, brings the other knight out, or tries the knight jump to the middle. Each has its own lesson.')]),
  'center': dict(h='Castle, and let the e-pawn go', b=[
    ('king', 'Castle next move, even if Black takes your e-pawn. Your rook lands on the open e-file while Black\'s king is still in the middle.'),
    ('pawns', 'If Black leaves the e-pawn alone, push the d-pawn at the knight.'),
    ('pieces', 'The dark bishop pins Black\'s king knight; the queen heads for the b-file to hit f7 and the b-pawn together.'),
    ('them', 'Black wants to grab your e-pawn and swap off your queen\'s knight.')]),
  'grab': dict(h='A pawn for open lines', b=[
    ('king', 'Yours is safe. Black\'s is still in the middle: open the e-file before it can castle.'),
    ('pawns', 'Push the d-pawn. It kicks Black\'s pieces and clears the long diagonal for your dark bishop.'),
    ('pieces', 'Rook to the e-file, dark bishop to the diagonal that stops Black castling, queen to the b-file.'),
    ('them', 'Black has to castle and give a pawn back. Every extra grab makes your attack stronger.')]),
  'nxc3-d5': dict(h='Both rooks on the open file', b=[
    ('king', 'Black\'s king is stuck in the middle. Keep the queen and both rooks aimed at it.'),
    ('pieces', 'Trades of rooks help Black; keep yours and use the open e-file and the checks your queen gets.'),
    ('watch', 'Black\'s queen hunts your loose pawns. Check every capture before a rook leaves the file.'),
    ('them', 'Black wants to swap a pair of rooks and walk the king to safety, where the extra pawns start to count.')]),
  'bxa1': dict(h='Collect the rook, then the king', b=[
    ('king', 'Black\'s king can\'t castle and has no cover. Keep your queen on the long diagonal and check it into the open.'),
    ('pieces', 'Bring the knight toward the king; the bishop takes on f7 when it gains time.'),
    ('pawns', 'Push the d-pawn: it opens more lines and chases Black\'s pieces.'),
    ('watch', 'Give your own king a square with one pawn move before Black\'s rooks come to life.')]),
  'trap-d5': dict(h='Take the c-pawn, then the rook', b=[
    ('target', 'Black castled long into your pieces. The bishop takes the c-pawn with check, then the rook behind it.'),
    ('pieces', 'Rook on the open c-file, queen on the light squares toward Black\'s king.'),
    ('watch', 'Don\'t trade queens: Black\'s king is the weak point.')]),
  'be7': dict(h='Win the loose knight, keep the king in the middle', b=[
    ('target', 'Black\'s knight on the edge has no guard and your queen hits it. Take it once the checks run out.'),
    ('king', 'Black\'s king can no longer castle. Rooks to the open files keep it in the middle.'),
    ('pieces', 'Swap the dark bishops, then the knight jumps toward the king.'),
    ('them', 'Black wants to trade queens and untangle. Keep yours.')]),
  'moller-bf6': dict(h='Keep checking: a draw at worst', b=[
    ('king', 'Black\'s king is in the open. Keep checking with the queen.'),
    ('them', 'With perfect defence it is a draw by repeated checks. One wrong king step and your rook joins with mate.'),
    ('watch', 'Don\'t stop checking to grab material: Black\'s queen and rooks are waiting to come back.')]),
  'moller-ne5': dict(h='Press on the knight, use the space', b=[
    ('pieces', 'Your dark bishop presses on the knight, with Black\'s pawn and rook lined up behind it. The knight in the middle jumps forward when it hits something.'),
    ('pawns', 'Your advanced d-pawn cramps Black. Support it with the c-pawn.'),
    ('them', 'Black wants to push the f-pawn and open lines toward your king.'),
    ('watch', 'Keep your queen guarded: Black\'s pieces line up on it quickly.')]),
  'quiet-d6': dict(h='The passed pawn is your trump', b=[
    ('pawns', 'Your d-pawn is passed and deep in Black\'s camp. Guard it and push it when you can.'),
    ('pieces', 'Rook behind the pawn on the d-file, dark bishop to the pin on Black\'s knight.'),
    ('target', 'Black\'s pieces are tied to stopping the pawn. Attack where they are not.'),
    ('them', 'Black wants to block the pawn with a piece and then win it.')]),
  'bb6': dict(h='Queens off, Black\'s pawns broken', b=[
    ('target', 'Black\'s doubled pawns and the weak squares beside its king.'),
    ('pieces', 'The knight takes a weak pawn with check; bishops out fast, rooks to the open files.'),
    ('king', 'With the queens gone your king can stay in the middle and help.'),
    ('them', 'Black is short of time to develop. Meet any check calmly and keep collecting.')]),
  'four-d6': dict(h='Pile up on the pinned knight', b=[
    ('target', 'Black\'s knight in the middle is pinned on the e-file. Attack it again with your knight.'),
    ('pieces', 'Rook stays on the e-file, bishop keeps pressing, knight comes out with tempo.'),
    ('watch', 'Black\'s only tries are checks and a grab near your king. Count them before you take.')]),
  'other-4th': dict(h='Space first, then the queenside', b=[
    ('pawns', 'Push the d-pawn past to gain space and kick the knight; then the queenside pawns roll.'),
    ('king', 'You are castled; Black is not. Open the center if it stays there.'),
    ('pieces', 'Rook to the e-file, the queen\'s knight out behind the c-pawn.'),
    ('them', 'Black wants to pin your knight and break in the middle.')]),
  'bb6-early': dict(h='A pawn up, Black can\'t castle', b=[
    ('king', 'Black\'s king has moved and can\'t castle. Castle yourself and open the f-file.'),
    ('pieces', 'Knight back into play, dark bishop out with tempo on the knight in the middle.'),
    ('target', 'f7 and the open king: your queen and the rook on the f-file both point there.'),
    ('watch', 'Black\'s knight in the middle hits your pawns; keep them guarded.')]),
  # ---------------------------------------------------------------- Two Knights
  'fried-liver': dict(h='Win the queen, then the knight', b=[
    ('target', 'The bishop check wins Black\'s queen. Take it, then the knight in the middle.'),
    ('king', 'You castled long; Black\'s king has no shelter. Keep the rooks on the open files.'),
    ('watch', 'Black\'s pawn beside your king: take it when it is safe.')]),
  'fried-liver-nb4': dict(h='Open lines toward the king', b=[
    ('king', 'Black\'s king sits on the queenside with no pawns in front of it. Open lines there.'),
    ('pawns', 'Push the d-pawn: it opens the long diagonal for your dark bishop.'),
    ('pieces', 'Dark bishop to the long diagonal, rooks to the open files, queen checks when they gain time.'),
    ('them', 'Black wants to trade queens and hide the king.')]),
  'two-knights-na5': dict(h='Keep the pawn, finish developing', b=[
    ('pawns', 'You are a pawn up. Keep it and trade pieces.'),
    ('king', 'Castle next; Black still has to untangle.'),
    ('target', 'Black\'s knight on the edge: bishop and queen can corner it.'),
    ('them', 'Black wants open lines and a lead in development. Every trade makes that harder.')]),
  'traxler': dict(h='Calm down, then collect', b=[
    ('king', 'You are castled and safe; Black\'s king has moved and can\'t castle.'),
    ('pieces', 'Knight home, then the d-pawn and bishop out. Swap off Black\'s bishop with a knight jump.'),
    ('watch', 'Black\'s rook and knight aim at f2. Keep it guarded and don\'t grab more.')]),
  'tk-sidelines': dict(h='A rook up: get developed', b=[
    ('pieces', 'Your knight in the corner is worth a pawn back. Develop everything else first, then castle.'),
    ('king', 'Castle soon. Black has nothing to show for the rook.'),
    ('watch', 'Black\'s queen and knights aim at f2 and your king. Keep it guarded.')]),
  'shilling': dict(h='Open the center at the stuck king', b=[
    ('king', 'Black\'s king has moved; yours is castled. Open the center.'),
    ('pieces', 'Rook and queen on the open files, dark bishop on the long diagonal at Black\'s king.'),
    ('target', 'The king and the knight guarding it.')]),
  'h6-3rd': dict(h='Black\'s king can\'t castle', b=[
    ('king', 'Black\'s king has moved. Open lines to keep it in the middle.'),
    ('pawns', 'Your center pawns are free: push the e-pawn and the f-pawn when ready.'),
    ('pieces', 'Dark bishop to the long diagonal, rook to the e-file.')]),
  'd6-3rd': dict(h='More space, easy development', b=[
    ('pieces', 'Knights in the middle, rooks to the center files, bishop aimed at f7.'),
    ('pawns', 'The f-pawn can push later for more space.'),
    ('them', 'Black wants to trade knights and break with the d-pawn.')]),
  'hungarian': dict(h='More space, easy development', b=[
    ('pieces', 'Knights in the middle, rooks to the center files, bishop aimed at f7.'),
    ('pawns', 'The f-pawn can push later for more space.'),
    ('them', 'Black is cramped and wants to trade pieces.')]),
  'rousseau': dict(h='Space and the open e-file', b=[
    ('pawns', 'Your e-pawn cramps Black. Keep it guarded.'),
    ('king', 'Castle and bring the rook to the e-file.'),
    ('target', 'Black\'s king side, weakened by the early f-pawn push.')]),
  # ---------------------------------------------------------------- Philidor & Petrov & other second moves
  'ph-main': dict(h='Castle long, then the pawn storm', b=[
    ('king', 'Castle long: the kings end up on opposite sides.'),
    ('pawns', 'Then the f-pawn and g-pawn march at Black\'s king.'),
    ('pieces', 'Queen and dark bishop line up; trade off the pieces that defend Black\'s king.'),
    ('them', 'Black is cramped and wants to break with the d-pawn or the c-pawn.')]),
  'ph-bg4': dict(h='Black\'s queenside is falling', b=[
    ('target', 'f7 and the b-pawn: your queen and bishop hit both.'),
    ('king', 'Castle long when ready; Black\'s king is still at home.'),
    ('pieces', 'Dark bishop pins Black\'s knight, then a rook to the open d-file.')]),
  'ph-nf6': dict(h='Castle long and press', b=[
    ('king', 'Castle long; your rook lands on the open d-file.'),
    ('target', 'Black\'s lone d-pawn.'),
    ('pieces', 'Swap the dark bishops if Black offers, then knights to the center.')]),
  'ph-nd7': dict(h='King hunt', b=[
    ('target', 'Black\'s king is in the open. Check with the queen and knight.'),
    ('king', 'Castle, then bring the rook to the f-file.'),
    ('watch', 'Don\'t trade queens: the attack is the point.')]),
  'ph-nc6': dict(h='Space on the queenside', b=[
    ('pawns', 'Your d-pawn and c-pawn take space. Push the c-pawn on to open the queenside.'),
    ('pieces', 'Knights out, bishop to the quiet square, castle.'),
    ('them', 'Black will push the f-pawn at your king side. Answer in the center.')]),
  'pt-main': dict(h='Undermine the knight in the middle', b=[
    ('pawns', 'The c-pawn hits Black\'s center. Trade it off and the knight in the middle loses its support.'),
    ('pieces', 'Knight out to attack that knight, rook to the e-file.'),
    ('target', 'Black\'s knight in the middle and the pawn behind it.')]),
  'pt-copy': dict(h='A pawn up with a pin', b=[
    ('pawns', 'You are a pawn up. Guard the e-pawn.'),
    ('king', 'Castle soon.'),
    ('pieces', 'Bishop pins the knight, queen stays central.')]),
  'pt-stafford': dict(h='A piece up and safe', b=[
    ('king', 'Castled and safe; f2 is guarded.'),
    ('pieces', 'Bring the knight out and trade pieces: every trade makes the extra piece count more.'),
    ('them', 'Black wants to push the f-pawn at your king. Meet it with a knight in the middle.')]),
  'pt-qe7': dict(h='Ahead in development', b=[
    ('king', 'Castle next. Black\'s queen sits in front of its own king.'),
    ('pieces', 'Rook to the e-file to pin the knight against the queen.'),
    ('target', 'Black\'s knight in the middle and the queen behind it.')]),
  'x-qf6': dict(h='Kick the queen, castle long', b=[
    ('king', 'Castle long; the rook comes to the d-file.'),
    ('pieces', 'Develop with threats on the queen; knights to the center.'),
    ('target', 'Black\'s queen keeps moving while you develop.')]),
  'x-bc5': dict(h='A pawn up with the center', b=[
    ('pawns', 'You are a pawn up with two pawns in the middle.'),
    ('pieces', 'Knight jumps to the hole in the middle, bishop out, castle.'),
    ('watch', 'Black\'s queen sits opposite your king on the e-file. Castle soon.')]),
  'x-f6': dict(h='Get the queen out, keep the rook', b=[
    ('target', 'You are a rook up. Get the queen out of the corner before it is trapped.'),
    ('watch', 'Black will try to shut your queen in with the knight and bishop. Keep a way out.'),
    ('pieces', 'Develop with tempo and castle.')]),
  'x-f5': dict(h='Attack the open king', b=[
    ('target', 'Black\'s king, opened by the f-pawn push. Queen check on the diagonal, then a rook to the e-file.'),
    ('pieces', 'Queen and knight together.'),
    ('watch', 'Black\'s knight in the middle can block; take it when it does.')]),
  'x-d5': dict(h='Win the e-pawn back with interest', b=[
    ('target', 'Black\'s e-pawn is weak; your knight and queen hit it.'),
    ('pawns', 'Keep your extra d-pawn. Black wants it back.'),
    ('king', 'Castle once the e-pawn falls.')]),
  # ---------------------------------------------------------------- Caro-Kann
  'ck-march': dict(h='Opposite sides: attack the king side', b=[
    ('king', 'You castled long; Black will castle short. It is a race.'),
    ('pawns', 'Your h-pawn already cramps Black\'s king side. The g-pawn joins it.'),
    ('pieces', 'Knight to the strong square in the middle, queen on the diagonal toward the king side, rooks to the center files.'),
    ('them', 'Black wants the c-pawn break and a queen trade.')]),
  'ck-h5': dict(h='The bishop is shut out', b=[
    ('target', 'Black\'s light bishop is stuck behind its pawns on the edge.'),
    ('pieces', 'Knights to the jump squares on the king side, rook to the e-file.'),
    ('pawns', 'The h-pawns are locked; the square in front of yours belongs to your knight.')]),
  'ck-bishop6': dict(h='Two bishops against broken pawns', b=[
    ('target', 'Black\'s doubled pawns and the holes left by the bishop.'),
    ('pieces', 'Both bishops on open diagonals.'),
    ('king', 'Castle long and push the g-pawn.')]),
  'ck-takes': dict(h='Two bishops against broken pawns', b=[
    ('target', 'Black\'s doubled pawns on the king side. Pile up on them.'),
    ('pieces', 'Bishops on open diagonals, knight to the center, queen to the light diagonal.'),
    ('king', 'Castle short; Black\'s king will feel your bishops.')]),
  'ck-nf6': dict(h='Healthier pawns, king-side play', b=[
    ('pawns', 'Your pawns are healthy. Black\'s extra king-side pawn can\'t make a passed pawn.'),
    ('pieces', 'Queen and light bishop on the diagonal at Black\'s king.'),
    ('king', 'Castle, then press on the king side.')]),
  'ck-quiet': dict(h='Kick the queen, castle long', b=[
    ('pieces', 'The bishop kicks the queen; queen to the middle, castle long.'),
    ('pawns', 'More space in the center. Push the d-pawn only with support.'),
    ('target', 'Black\'s queen keeps moving.')]),
  'ck-nf6-3': dict(h='Attack the pawn in the middle', b=[
    ('target', 'Black\'s pawn in the middle is weak; knight and queen hit it.'),
    ('pawns', 'Your e-pawn cramps Black. Keep it guarded; the f-pawn can join later.'),
    ('king', 'Castle short.')]),
  'ck-e6-3': dict(h='Two bishops and space', b=[
    ('pieces', 'You have both bishops. Open the position.'),
    ('pawns', 'Push the h-pawn and the a-pawn to make Black\'s pawns move.'),
    ('king', 'Castle short later, behind pawns.')]),
  # ---------------------------------------------------------------- Sicilian with the c-pawn
  'sc-push': dict(h='Black\'s knights have no squares', b=[
    ('target', 'Black\'s knights are pushed back. Keep them out with your pawns.'),
    ('pawns', 'Your d-pawn and e-pawn are the trumps. Keep them guarded and push when it kicks something.'),
    ('pieces', 'Develop fast: knight out, light bishop to an active diagonal.')]),
  'sc-e5push': dict(h='Space, and a bad bishop for Black', b=[
    ('pawns', 'Your d-pawn cramps Black, and Black\'s light bishop is stuck behind its own pawn.'),
    ('pieces', 'Bishop to an active diagonal, knight toward the center through the queenside.'),
    ('king', 'Castle short.')]),
  'sc-e6': dict(h='The French chain, with your bishops out', b=[
    ('pawns', 'Your pawn chain points at Black\'s king. Keep the e-pawn strongly guarded.'),
    ('pieces', 'Light bishop and queen at the king side; castle, then the h-pawn can push.'),
    ('them', 'Black hits the chain with the f-pawn. Take only if it opens lines for you.')]),
  'sc-d5': dict(h='A queen up: trade down', b=[
    ('target', 'You won the queen. Castle, develop and trade pieces.'),
    ('watch', 'Black\'s rooks come to the open files. Keep your back rank safe.')]),
  'sc-d6': dict(h='The big center', b=[
    ('pawns', 'Push the d-pawn at the knight when it comes out; your center gains space.'),
    ('pieces', 'Bishops to active diagonals, rooks to the center files.'),
    ('them', 'Black wants the pin on your knight and pressure on the d-pawn.')]),
  'sc-e6p': dict(h='The French chain', b=[
    ('pawns', 'Guard the d-pawn: it is the base of your chain.'),
    ('pieces', 'Bishop to the quiet square, castle, the queen\'s knight comes round to support the d-pawn.'),
    ('them', 'Black hits the base of the chain with the c-pawn and the queen.')]),
  'sc-e5': dict(h='Pressure on f7', b=[
    ('target', 'f7 and Black\'s knight in the middle.'),
    ('pieces', 'Castle, then queen and bishop hit f7.'),
    ('watch', 'Black\'s center pawns can roll forward. Keep your pieces active and hit them.')]),
  'sc-qd5': dict(h='Easy development', b=[
    ('pieces', 'Bishop to an active diagonal, knight round to the center, rook to the d-file.'),
    ('pawns', 'Your d-pawn may end up alone. Keep pieces near it.'),
    ('them', 'Black wants to trade on the d-pawn and press against it.')]),
  'sc-g6': dict(h='Push the knight around', b=[
    ('pawns', 'Your d-pawn kicks the knight. Keep using pawns to take its squares.'),
    ('pieces', 'Dark bishop to the diagonal against Black\'s long bishop, knight out, castle.')]),
  'sc-nf6': dict(h='Active pieces', b=[
    ('pieces', 'Bishop on the f7 diagonal, queen to the queenside when it gains time, castle.'),
    ('pawns', 'Your e-pawn is far forward. Keep it guarded.')]),
  # ---------------------------------------------------------------- Scandinavian, Pirc, French, rare
  'sd-qa5': dict(h='Castle long, then the pawns go', b=[
    ('king', 'Castle long; queen and bishop guard it.'),
    ('pawns', 'Then the g-pawn and h-pawn push at Black\'s king.'),
    ('pieces', 'Knight jump at the queen whenever it gains time.'),
    ('them', 'Black wants to trade queens and win your d-pawn.')]),
  'sd-qd8': dict(h='Space and the center', b=[
    ('pieces', 'Bishop pins, a knight jumps into the center, rook to the e-file.'),
    ('pawns', 'Your d-pawn controls the center. Support it with the c-pawn.'),
    ('king', 'You are castled; Black still has to.')]),
  'sd-qe6': dict(h='Ahead in development', b=[
    ('pieces', 'Castle, then rook to the e-file: Black\'s queen stands in front of its king.'),
    ('pawns', 'Push the d-pawn at the knight.'),
    ('target', 'The queen in front of the king.')]),
  'sd-qe5': dict(h='Kick the queen again', b=[
    ('pieces', 'Knight out with tempo, castle, rook to the e-file.'),
    ('pawns', 'The d-pawn kicked the queen; your center grows.')]),
  'sd-qd6': dict(h='Chase the bishop and the queen', b=[
    ('pawns', 'Push the g-pawn at the bishop if it stays; a knight jumps at the queen.'),
    ('pieces', 'Light bishop to the long diagonal, castle.')]),
  'sd-b4': dict(h='Develop fast and hit the queen', b=[
    ('them', 'Black is a pawn up. Develop quickly and chase the queen.'),
    ('pieces', 'Knight and bishop at the queen, then castle.')]),
  'sd-nf6': dict(h='Two pawns in the middle', b=[
    ('pawns', 'Your d-pawn and c-pawn own the center. Push the d-pawn when it gains space.'),
    ('pieces', 'Castle, knight out, queen to the queenside to hit the b-pawn.')]),
  'sd-c6': dict(h='A pawn up: develop and trade', b=[
    ('pawns', 'You are a pawn up. Develop, castle, and trade pieces.'),
    ('pieces', 'Bishop pins the knight, rook to the e-file.')]),
  'pc-150': dict(h='Swap the bishop, then storm the king', b=[
    ('pieces', 'Your dark bishop trades off Black\'s long bishop.'),
    ('pawns', 'Then the h-pawn and g-pawn push at Black\'s king and open the h-file.'),
    ('them', 'Black attacks your king on the queenside. Be faster.')]),
  'pc-modern': dict(h='Swap the bishop, then storm the king', b=[
    ('pieces', 'Your dark bishop trades off Black\'s long bishop.'),
    ('pawns', 'Then the h-pawn and g-pawn push at Black\'s king.'),
    ('king', 'Castle long first.')]),
  'pc-e5': dict(h='Black\'s king can\'t castle', b=[
    ('king', 'Without queens your king is safe; Black\'s is stuck in the middle.'),
    ('target', 'f7: your bishop hits it.'),
    ('pieces', 'Knights out, rooks to the d-file.')]),
  'pc-other': dict(h='The French chain', b=[
    ('pawns', 'Guard the d-pawn, the base of your chain.'),
    ('pieces', 'Bishop to the quiet square, castle, knight round to support the center.')]),
  'fr-qb6': dict(h='Space on both sides', b=[
    ('pawns', 'Your queenside pawns gain space; Black\'s queen is short of squares.'),
    ('pieces', 'Dark bishop to the long diagonal, rook to the c-file, knight back to the center.'),
    ('them', 'Black will hit your e-pawn with the f-pawn.')]),
  'fr-other5': dict(h='A space edge', b=[
    ('pawns', 'Keep the d-pawn guarded; it is the base of the chain.'),
    ('pieces', 'Knight round to support the center, bishop to an active diagonal.'),
    ('them', 'Black presses on the d-pawn with the queen and knights.')]),
  'fr-early': dict(h='Back in the main plan', b=[
    ('pawns', 'The b-pawn push gains queenside space; keep the d-pawn guarded.'),
    ('pieces', 'Bishop out, castle, knight round to the center.')]),
  'fr-c5': dict(h='The French chain', b=[
    ('pawns', 'Guard the d-pawn, the base of your chain.'),
    ('pieces', 'Bishop to the quiet square, castle, knight round to support the center.')]),
  'rr-owen': dict(h='Big center, guarded', b=[
    ('pawns', 'Push the e-pawn past the knight when it gains space.'),
    ('pieces', 'Castle, rook behind the center pawns.')]),
  'rr-nimzo': dict(h='Back in your Italian', b=[
    ('pawns', 'Small c-pawn move, then the d-pawn two squares.'),
    ('king', 'Castle short.'),
    ('target', 'f7.')]),
  'rr-alekhine': dict(h='Two bishops and space', b=[
    ('pawns', 'The c-pawn kicks the knight; your pawns take space.'),
    ('pieces', 'Keep the position open for the bishops.')]),
  'rr-stgeorge': dict(h='Hit the advanced pawns', b=[
    ('pawns', 'Push the a-pawn and c-pawn at Black\'s queenside pawns.'),
    ('pieces', 'Knight out, rook to the e-file.')]),
}

B = {
  # ---------------------------------------------------------------- the Italian
  'bi-main': dict(h='Pressure on the lone d-pawn', b=[
    ('target', 'White\'s d-pawn is alone and needs guarding all game.'),
    ('pieces', 'Your knight sits in front of it where no pawn can kick it. Bishop out, rooks to the d-file and the e-file.'),
    ('them', 'White wants the knight jump to the center and pressure on your king side.'),
    ('watch', 'White\'s queen and bishop can line up on f7. Keep it guarded.')]),
  'bi-qxd2': dict(h='A pawn up: castle and keep it', b=[
    ('king', 'Castle next.'),
    ('pieces', 'Guard the knight in the middle, then bring the light bishop out.'),
    ('pawns', 'Your extra pawn is in the center. Keep it, and trade pieces.')]),
  'bi-nc3': dict(h='A pawn up: hold the knight in the middle', b=[
    ('pieces', 'Your knight in the middle is strong. Support it, and trade White\'s attacking pieces.'),
    ('king', 'You are castled. Watch for the bishop and queen against your king.'),
    ('them', 'White wants to open lines with the f-pawn for the lost pawn.')]),
  'bi-e5': dict(h='Equal and active', b=[
    ('king', 'Castle next.'),
    ('pawns', 'Break with the f-pawn to hit White\'s far-advanced e-pawn.'),
    ('pieces', 'Knight in the middle, bishop on its diagonal.')]),
  'bi-slow': dict(h='Your setup, then the knight jump', b=[
    ('pieces', 'Light bishop out, then the knight jumps to the edge to trade off White\'s Italian bishop.'),
    ('pawns', 'Later the f-pawn or d-pawn break opens the position.'),
    ('them', 'White wants to reroute the knight to the king side and push the d-pawn.')]),
  'bi-ng5': dict(h='White wasted time: develop and break', b=[
    ('pieces', 'Bring the queen\'s knight round to the king side; swap White\'s bishop if it offers.'),
    ('pawns', 'Later the d-pawn break in the middle.'),
    ('watch', 'Your h-pawn move left a hole. Keep a knight near your king.')]),
  'bi-bg5': dict(h='Break the pin', b=[
    ('pawns', 'The g-pawn can push to kick the bishop if you castle long or keep the king in the middle.'),
    ('pieces', 'Light bishop out, queen to the e-file; castle on the side that is safe.'),
    ('them', 'White wants to keep the pin and bring the knight to the hole on the king side.')]),
  'bi-4n': dict(h='Take the bishop, then castle', b=[
    ('pieces', 'Your knight takes White\'s Italian bishop: you get the two bishops.'),
    ('king', 'Castle next.'),
    ('pawns', 'Then the d-pawn strike in the center.')]),
  'bi-oo': dict(h='Your setup again', b=[
    ('king', 'Castle next.'),
    ('pieces', 'Knight jumps to the edge to trade White\'s bishop, light bishop to the e-file side.'),
    ('pawns', 'The d-pawn or f-pawn break later.')]),
  'bi-evans': dict(h='A pawn up: develop and trade', b=[
    ('pieces', 'Knight out, castle. Your knight on the edge can take White\'s bishop.'),
    ('pawns', 'You are a pawn up. Trade pieces.'),
    ('them', 'White wants open lines and an attack for the pawn.')]),
  'bi-d4': dict(h='A pawn up: develop and trade', b=[
    ('king', 'Castle next.'),
    ('pieces', 'Small d-pawn move, light bishop out, trade pieces.'),
    ('them', 'White wants an attack with the f-pawn for the pawn.')]),
  'bi-cheap': dict(h='A piece up: castle and trade', b=[
    ('king', 'Develop and castle.'),
    ('pieces', 'Trade pieces: every trade makes the extra piece count more.'),
    ('watch', 'White will throw pawns and pieces at your king. Keep it covered.')]),
  # ---------------------------------------------------------------- Ruy Lopez
  'br-oo': dict(h='Hold the center, then strike', b=[
    ('pawns', 'Keep the e-pawn. Your d-pawn strike comes later.'),
    ('pieces', 'Small d-pawn move, then the light bishop out.'),
    ('them', 'White wants the big center. Don\'t give up your e-pawn for free.')]),
  'br-d3': dict(h='Knight round to the king side', b=[
    ('pieces', 'The queen\'s knight comes round to the king side; bishop steps back to keep its diagonal.'),
    ('pawns', 'The c-pawn and d-pawn prepare a break in the center.'),
    ('them', 'White wants the slow center push. Meet it with your own.')]),
  'br-nc3': dict(h='Your setup again', b=[
    ('pieces', 'Bishop steps back if the knight jumps at it. Light bishop out.'),
    ('pawns', 'Later the d-pawn break.')]),
  'br-bxc6': dict(h='Queens off: the two bishops', b=[
    ('king', 'Castle; without queens your king is safe either way.'),
    ('pieces', 'Your two bishops are the long-term edge. Open the position.'),
    ('pawns', 'Your queenside pawns can still create a passed pawn on the other side.')]),
  # ---------------------------------------------------------------- Scotch & center gambits
  'bs-classical': dict(h='Rook on the open file, knight round', b=[
    ('king', 'Castled long: the king is safe behind the queenside pawns.'),
    ('pieces', 'The king\'s knight comes out and round to the middle; the rook takes the open d-file.'),
    ('target', 'White\'s king side, weakened by the f-pawn move. Your queen and bishop aim there.'),
    ('them', 'White wants to castle long too and push the king-side pawns.')]),
  'bs-classical-be3': dict(h='The small d-pawn, then the knight jumps', b=[
    ('pawns', 'Small d-pawn move next, then the f-pawn break in the center.'),
    ('pieces', 'Your queen can shift to the king side and the f-pawn joins it.'),
    ('them', 'White wants to trade on your knight and take the open file.')]),
  'bs-classical-c3': dict(h='Your center, your space', b=[
    ('king', 'Castle next.'),
    ('pawns', 'Your d-pawn takes back toward the middle and owns the center.'),
    ('pieces', 'Queen to the middle, bishop to the long road; rooks to the open files.')]),
  'bs-classical-nb3': dict(h='Castle, then the d-pawn', b=[
    ('king', 'Castle next.'),
    ('pawns', 'Then the d-pawn strike.'),
    ('pieces', 'If the bishop takes your knight, your queen joins the attack on f2.')]),
  'bs-gambit': dict(h='Your Italian: pressure the d-pawn', b=[
    ('target', 'White\'s d-pawn will be alone. Your knight sits in front of it.'),
    ('king', 'Castle next.'),
    ('pieces', 'Light bishop pins the knight, queen to the d-file.')]),
  'bs-goring': dict(h='Pressure on the lone d-pawn', b=[
    ('target', 'White\'s d-pawn is alone.'),
    ('king', 'Castle long or short; the queen trade is fine for you.'),
    ('pieces', 'Rooks to the d-file, knight in front of the d-pawn.')]),
  'bs-center': dict(h='Ahead in development', b=[
    ('pawns', 'The d-pawn strike opens the e-file for your rook.'),
    ('pieces', 'Your bishop can trade on the knight to double White\'s pawns.'),
    ('target', 'White\'s king castled long. Your pieces aim there.')]),
  'bs-danish': dict(h='Pressure on the lone d-pawn', b=[
    ('target', 'White\'s d-pawn is alone. Pile up on it.'),
    ('pieces', 'Trade your light bishop for the knight that guards it, then the queen hits it.'),
    ('king', 'Castle long or short after the trades.')]),
  'bs-d4move': dict(h='Back in your Scotch', b=[
    ('pieces', 'Queen joins the bishop against f2 if the knight trade comes.'),
    ('pawns', 'Take back toward the middle with the d-pawn after any trade.'),
    ('king', 'Castle long or short when ready.')]),
  # ---------------------------------------------------------------- Four Knights, Vienna & quiet lines
  'bv-spanish': dict(h='Your Spanish setup again', b=[
    ('pieces', 'Bishop steps back if the knight jumps at it. Light bishop out.'),
    ('pawns', 'Later the d-pawn break.'),
    ('them', 'White wants the pin on your knight. Ask the bishop with the edge pawn.')]),
  'bv-scotch4n': dict(h='Free pieces, equal center', b=[
    ('pieces', 'Light bishop out, rook to the e-file.'),
    ('pawns', 'Your c-pawn can join to make a strong center.'),
    ('watch', 'White\'s bishop pin on your knight: be ready to break it.')]),
  'bv-italian4n': dict(h='Your Italian setup', b=[
    ('king', 'Castle next.'),
    ('pieces', 'Bishop steps back to keep its diagonal; knight round to the king side.'),
    ('them', 'White\'s knight in the middle wants trades. Let it.')]),
  'bv-quiet4n': dict(h='You have the center', b=[
    ('pieces', 'Bishop out, castle.'),
    ('pawns', 'Your e-pawn and the knight in the middle hold the center.'),
    ('them', 'White wants to trade knights and press your e-pawn.')]),
  'bv-bc5': dict(h='Castle, then trade the bishop', b=[
    ('king', 'Castle next, or push the g-pawn first to break the pin if White keeps it.'),
    ('pieces', 'The knight jumps to the edge to trade off White\'s Italian bishop.'),
    ('them', 'White\'s knight wants to jump at your bishop. Keep a retreat ready.')]),
  'bv-f4bc5': dict(h='Trade the bishop, then castle', b=[
    ('pieces', 'Your knight takes White\'s Italian bishop; then castle.'),
    ('king', 'White\'s king can\'t castle short while your bishop eyes its path.'),
    ('pawns', 'Later the d-pawn break opens the center against the uncastled king.')]),
  'bv-vmisc': dict(h='Back in your Spanish lesson', b=[
    ('king', 'Castle next.'),
    ('pawns', 'Then the small d-pawn move guards your e-pawn.'),
    ('pieces', 'Bishop steps back if a knight jumps at it.')]),
  'bv-ponziani': dict(h='Equal and free', b=[
    ('pieces', 'Bishop out, castle; your knight in the middle is strong.'),
    ('target', 'White\'s far-advanced e-pawn.')]),
  'bv-d3': dict(h='You own the center', b=[
    ('pieces', 'Bishop out, castle.'),
    ('pawns', 'Keep the knight in the middle; the c-pawn can support it.')]),
  'bv-tricks': dict(h='A piece up: develop', b=[
    ('pieces', 'Develop and castle; trade pieces.'),
    ('watch', 'White\'s pawns will chase your knights. Keep them safe.')]),
  # ---------------------------------------------------------------- early attacks
  'ba-qh5': dict(h='Trade the bishop, then break', b=[
    ('pieces', 'The knight jumps to the edge to trade off White\'s Italian bishop.'),
    ('pawns', 'Then the d-pawn or the f-pawn break.'),
    ('them', 'White\'s queen is out early. Develop with threats on it.')]),
  'ba-qh5-other': dict(h='Develop with threats', b=[
    ('king', 'Castle next.'),
    ('pieces', 'Every move that hits White\'s queen gains time.'),
    ('pawns', 'The d-pawn strike in the center.')]),
  'ba-kgd': dict(h='Trade the bishop, then castle', b=[
    ('pieces', 'Your knight takes White\'s Italian bishop; then castle.'),
    ('king', 'White\'s king can\'t castle short while your bishop eyes its path.'),
    ('pawns', 'Later the d-pawn break opens the center against the uncastled king.'),
    ('watch', 'If White plays the small c-pawn move, the knight jump loses to a queen check. Castle instead.')]),
  'ba-bc4': dict(h='Your Italian setup', b=[
    ('pieces', 'Small d-pawn move, castle; the knight jumps at the bishop later.'),
    ('pawns', 'The d-pawn break when White commits.')]),
  # ---------------------------------------------------------------- other first moves
  'bo-english': dict(h='Trade the knight, then strike', b=[
    ('pieces', 'Bishop takes the knight to double White\'s pawns.'),
    ('pawns', 'Your e-pawn cramps White; the d-pawn joins later.'),
    ('them', 'White wants to undermine your e-pawn with the d-pawn.')]),
  'bo-english2': dict(h='Your center, quick development', b=[
    ('pieces', 'Knight out, bishop out, castle.'),
    ('pawns', 'Your e-pawn holds the center.')]),
  'bo-reti': dict(h='The Slav setup', b=[
    ('pieces', 'Queen\'s knight out, bishop to its active square, castle.'),
    ('pawns', 'The e-pawn and c-pawn hold the center.')]),
  'bo-g3': dict(h='Take the center', b=[
    ('pieces', 'Knights out, bishop out, castle.'),
    ('pawns', 'Your e-pawn and d-pawn own the center.')]),
  'bo-e3': dict(h='Equal and open', b=[
    ('pieces', 'Knight out, bishop out, castle.')]),
  'bo-b3': dict(h='Take the center', b=[
    ('pieces', 'Knight out, castle; guard the e-pawn against the long bishop.')]),
  'bo-f4': dict(h='The Slav setup against the f-pawn', b=[
    ('king', 'Castle next.'),
    ('pieces', 'Queen\'s knight out. Your bishop outside the chain watches the middle squares.'),
    ('pawns', 'Later the c-pawn goes two squares.'),
    ('them', 'White wants a knight on the middle square in front of the f-pawn. Challenge it with your queen\'s knight.')]),
  'bo-misc': dict(h='Develop and castle', b=[
    ('king', 'Castle next.'),
    ('pawns', 'The d-pawn and c-pawn take the center.')]),
  # ---------------------------------------------------------------- Queen's Gambit
  'bsl-slow': dict(h='Castle, then the e-pawn or c-pawn break', b=[
    ('king', 'Castle next.'),
    ('pawns', 'Then your e-pawn break, or the c-pawn break, frees your game.'),
    ('pieces', 'Your knights guard each other; the queen can go to the c-file side.'),
    ('them', 'White wants the e-pawn push into the middle. Take it at once and trade knights.'),
    ('watch', 'If the c-pawn pushes at your bishop, step back one square on the same diagonal.')]),
  'bsl-slow2': dict(h='Castle, then the e-pawn or c-pawn break', b=[
    ('king', 'Castle next.'),
    ('pawns', 'Then your e-pawn break, or the c-pawn break, frees your game.'),
    ('pieces', 'Your knights guard each other; the queen can go to the c-file side.'),
    ('them', 'White wants the e-pawn push into the middle. Take it at once and trade knights.'),
    ('watch', 'If the c-pawn pushes at your bishop, step back one square on the same diagonal.')]),
  'bsl-main': dict(h='Hold the pawn, develop', b=[
    ('pawns', 'You are a pawn up for now. Keep the queenside pawns together.'),
    ('pieces', 'Knight back out, bishop out, castle.'),
    ('them', 'White wants to win the pawn back and push the d-pawn.')]),
  'bsl-exch': dict(h='Symmetrical and solid', b=[
    ('pieces', 'Bishop out, castle, rook to the c-file.'),
    ('pawns', 'Keep the d-pawn guarded.')]),
  'bsl-pin': dict(h='A piece up: castle and trade', b=[
    ('king', 'Castle as soon as you can.'),
    ('pieces', 'Trade pieces; the extra bishop decides.'),
    ('watch', 'White will push pawns at your king. Keep it covered.')]),
  'bsl-bf4': dict(h='Hold the extra pawn', b=[
    ('pawns', 'Keep the queenside pawns together; you are a pawn up.'),
    ('pieces', 'Knight out, bishop out, castle.')]),
  'bln-main': dict(h='The c-pawn break', b=[
    ('pawns', 'Next the c-pawn hits the center.'),
    ('pieces', 'Queen\'s knight out, rooks to the c-file and the d-file.'),
    ('them', 'White wants the knight jump to the middle and the e-pawn push.')]),
  'bln-c4': dict(h='The Slav triangle against the London', b=[
    ('king', 'Castle next.'),
    ('pieces', 'Queen\'s knight out; the queen is safe in the middle of your triangle.'),
    ('pawns', 'Later your e-pawn break frees your game.'),
    ('them', 'White wants the queen move at your b-pawn or the c-pawn push. The triangle holds both.')]),
  'bln-nf3': dict(h='Trade the bishops, castle', b=[
    ('pieces', 'Offer the dark bishop trade, then castle.'),
    ('pawns', 'Then the c-pawn break.')]),
  'bln-jobava': dict(h='Castle, then the c-pawn break', b=[
    ('king', 'Castle next.'),
    ('pawns', 'Then the c-pawn or e-pawn break.')]),
  'bdx-colle': dict(h='Castle; your pieces stand as in the Slav', b=[
    ('king', 'Castle next.'),
    ('pieces', 'The knight comes to the king\'s side and hits the queen; rooks to the middle files.'),
    ('pawns', 'Once you are castled, the c-pawn goes one more square and hits the center.'),
    ('them', 'White has the queen in the middle but no attacking bishop left. Trades favour you.')]),
  'bdx-torre': dict(h='Trade the bishop, castle', b=[
    ('pieces', 'Your knight in the middle is strong; trade the dark bishops.'),
    ('king', 'Castle next.')]),
  'bdx-veresov': dict(h='Two bishops, safe king', b=[
    ('king', 'Castle next; the e-pawn recapture keeps your king safe.'),
    ('pieces', 'Your dark bishop has a free road.')]),
  'bdx-bdg': dict(h='Keep the extra pawn or return it well', b=[
    ('pieces', 'Develop quickly; trade queens if White offers.'),
    ('pawns', 'Your extra pawn is the long-term edge.')]),
  'bdx-misc': dict(h='Castle, then the c-pawn break', b=[
    ('king', 'Castle next.'),
    ('pawns', 'Then the c-pawn break.')]),
}
