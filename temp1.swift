let footerHeight = currentFooterHeight
let bodyHeight = spreadsheetView.bounds.height - footerHeight

tableBodyShadowView.frame = CGRect(
    x: spreadsheetView.frame.minX,
    y: spreadsheetView.frame.minY,
    width: spreadsheetView.bounds.width,
    height: bodyHeight
)


tableBodyShadowView.layer.shadowColor = UIColor.black.cgColor
tableBodyShadowView.layer.shadowOpacity = 0.15
tableBodyShadowView.layer.shadowOffset = CGSize(width: 0, height: 2)
tableBodyShadowView.layer.shadowRadius = 6
tableBodyShadowView.layer.shadowPath = UIBezierPath(
    roundedRect: tableBodyShadowView.bounds,
    cornerRadius: 8
).cgPath


let bodyHeight = spreadsheetView.bounds.height - footerHeight

tableBodyShadowView.frame = CGRect(
    x: spreadsheetView.frame.minX,
    y: spreadsheetView.frame.minY,
    width: spreadsheetView.bounds.width,
    height: bodyHeight
).insetBy(dx: 0, dy: 0)

// 关键：让 shadowPath 只按 bodyHeight 画，但 view 本身允许阴影扩散
tableBodyShadowView.layer.shadowPath = UIBezierPath(
    roundedRect: CGRect(
        x: 0,
        y: 0,
        width: spreadsheetView.bounds.width,
        height: bodyHeight
    ),
    cornerRadius: 8
).cgPath




let bodyBottomShadowView = UIView()
bodyBottomShadowView.backgroundColor = .clear
bodyBottomShadowView.layer.shadowColor = UIColor.black.cgColor
bodyBottomShadowView.layer.shadowOpacity = 0.15
bodyBottomShadowView.layer.shadowOffset = CGSize(width: 0, height: 2)
bodyBottomShadowView.layer.shadowRadius = 6

bodyBottomShadowView.frame = CGRect(
    x: spreadsheetView.frame.minX,
    y: spreadsheetView.frame.maxY - footerHeight - 1,
    width: spreadsheetView.bounds.width,
    height: 1
)



view.addSubview(tableShadowView)
view.addSubview(spreadsheetView)

spreadsheetView.snp.makeConstraints { make in
    make.edges.equalTo(view.safeAreaLayoutGuide)
}

tableShadowView.snp.makeConstraints { make in
    make.edges.equalTo(spreadsheetView)
}
